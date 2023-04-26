import json
import logging
import os
import socket

MULTICAST_TTL = 1
SOCK_TIMEOUT = 10

config: dict = None
bench_request_msg: bytes = None

logger = logging.getLogger(__name__)


def process_unicast_request(
    bench: str, client_sock: socket.socket, client_addr: tuple[str, str]
) -> bytes:
    bench_conf = config[bench]
    bench_addr = socket.gethostbyname(bench_conf["container"]), bench_conf["port"]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as bench_sock:
        logger.info(f"Redirecting request to target bench {bench_addr}")
        bench_sock.sendto(bench_request_msg, bench_addr)

        bench_sock.settimeout(SOCK_TIMEOUT)
        while True:
            try:
                resp, addr = bench_sock.recvfrom(1024)
                if bench_addr == addr:
                    client_sock.sendto(resp, client_addr)
                    break

                logger.info(
                    "Received a msg on bench socket from someone other than the bench itself..."
                    f"Addr: {addr}, contents: {resp}"
                )

            except TimeoutError:
                logger.info("Target bench didn't sespond within a timeout")
                client_sock.sendto(
                    b"The server couldn't process your request in time, please try again\n",
                    client_addr,
                )

        logger.info(f"Unicast request handled from {client_addr} with response: {resp}")


def process_multicast_request(
    client_sock: socket.socket,
    multicast_sock: socket.socket,
    multicast_addr: tuple[str, int],
    client_addr: tuple[str, int],
) -> None:
    multicast_sock.sendto(bench_request_msg, multicast_addr)
    for _ in range(len(config)):
        resp, _ = multicast_sock.recvfrom(1024)
        client_sock.sendto(resp, client_addr)
        logger.info(f"Multicast request in process: sent {resp} to {client_addr}")

    logger.info(f"Multicast request handled from {client_addr}")


def serve(
    client_sock: socket.socket,
    multicast_sock: socket.socket,
    multicast_addr: tuple[str, int],
) -> None:
    # expected msg: get_result <target_format>
    def parse_msg(msg: str) -> str:
        args = msg.decode().split()

        if (
            len(args) != 2
            or args[0] != "get_result"
            or (args[1] not in config and args[1] != "all")
        ):
            return None

        return args[1]

    while True:
        msg, client_addr = client_sock.recvfrom(1024)
        logger.info(f"Received {msg} from {client_addr}")

        target_format = parse_msg(msg)
        if target_format is None:
            resp = (
                "Invalid request, available options are:\n"
                "get_result all\n"
                "get_result <format>\n"
                "Available formats: \n"
                f"{', '.join(config.keys())}\n"
            )

            client_sock.sendto(resp.encode(), client_addr)
            logger.info(
                f"Handled invalid request from {client_addr} with response: {resp.encode()}"
            )
            continue

        if target_format != "all":
            logger.info(f"Handling unicast request from {client_addr}")
            process_unicast_request(target_format, client_sock, client_addr)
        else:
            logger.info(f"Handling multicast request from {client_addr}")
            process_multicast_request(
                client_sock, multicast_sock, multicast_addr, client_addr
            )


if __name__ == "__main__":
    port = int(os.environ["PORT"])
    multicast_addr = os.environ["MULTICAST_GROUP"], int(os.environ["MULTICAST_PORT"])
    bench_request_msg = os.environ["BENCH_REQUEST_MSG"].encode()
    config_path = os.environ["CONFIG"]

    with open(config_path, "r") as f:
        config = json.load(f)

    logging.basicConfig()
    logger.setLevel(logging.INFO)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_addr = ("0.0.0.0", int(port))
    client_sock.bind(client_addr)

    multicast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    multicast_sock.settimeout(SOCK_TIMEOUT)

    logger.info(f"Proxy now listening for requests on {client_addr}")
    serve(client_sock, multicast_sock, multicast_addr)
