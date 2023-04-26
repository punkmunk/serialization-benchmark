from sample_data.data import generate_sample_data
from serializer.base import BaseSerializer
from serializer.get_serializer import get_serializer
from serializer.proto.school_pb2 import School as SchoolProto

import json
import logging
from multiprocessing import Process
import os
import socket
import struct
import timeit


TOTAL_ITER_COUNT = 1000
ITER_REPEAT = 5
ITER_NUMBER = TOTAL_ITER_COUNT // ITER_REPEAT

serializer: BaseSerializer = None
sample_data: dict | SchoolProto = None
serialized_data: bytes = None
ser_format: str = None
bench_request_msg: bytes = None

logger = logging.getLogger(__name__)


def run_bench() -> str:
    # min gives a lower bound on how fast a given snippet can run
    # calculating mean and variance is discouraged
    # refer to https://docs.python.org/3/library/timeit.html for details
    # (Note under repeat() function documentation)
    ser_time = 1000 * min(
        timeit.repeat(
            lambda: serializer.serialize(sample_data),
            number=ITER_NUMBER,
            repeat=ITER_REPEAT,
        )
    )
    de_time = 1000 * min(
        timeit.repeat(
            lambda: serializer.deserialize(serialized_data),
            number=ITER_NUMBER,
            repeat=ITER_REPEAT,
        )
    )

    return (
        f"{ser_format} - {len(serialized_data)} - {ser_time:.0f}ms - {de_time:.0f}ms\n"
    )


def serve(sock: socket.socket) -> None:
    logger.info(
        f"Now listening for {ser_format} bench requests on {sock.getsockname()}"
    )

    while True:
        msg, addr = sock.recvfrom(1024)
        logger.info(f"Received {msg} from {addr}")
        if msg != bench_request_msg:
            sock.sendto(
                b"Invalid request, valid options are:\n" + bench_request_msg + b"\n"
            )
            continue

        bench_result = run_bench().encode()
        sock.sendto(bench_result, addr)
        logger.info(f"Handled request from {addr} with response: {bench_result}")


if __name__ == "__main__":
    ser_format = os.environ["SER_FORMAT"]
    multicast_addr = os.environ["MULTICAST_GROUP"], int(os.environ["MULTICAST_PORT"])
    bench_request_msg = os.environ["BENCH_REQUEST_MSG"].encode()
    config_path = os.environ["CONFIG"]

    with open(config_path, "r") as f:
        config = json.load(f)[ser_format]

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    serializer = get_serializer(ser_format)
    sample_data = serializer.prepare_data(generate_sample_data())
    serialized_data = serializer.serialize(sample_data)
    assert sample_data == serializer.deserialize(serialized_data)

    unicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    unicast_addr = ("0.0.0.0", config["port"])
    unicast_sock.bind(unicast_addr)

    multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_sock.bind(multicast_addr)
    group = socket.inet_aton(multicast_addr[0])
    multicast_sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        struct.pack("4sL", group, socket.INADDR_ANY),
    )

    processes = [
        Process(target=serve, args=(unicast_sock,)),
        Process(target=serve, args=(multicast_sock,)),
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
