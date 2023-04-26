from .base import BaseSerializer
from .json_serializer import JSONSerializer
from .pickle_serializer import PickleSerializer
from .xml_serializer import XMLSerializer
from .yaml_serializer import YAMLSerializer
from .msgpack_serializer import MsgPackSerializer
from .avro_serializer import AvroSerializer
from .proto_serializer import ProtoSerializer

import logging


def get_serializer(format: str) -> BaseSerializer:
    match format:
        case "Pickle":
            return PickleSerializer()
        case "JSON":
            return JSONSerializer()
        case "XML":
            return XMLSerializer()
        case "YAML":
            return YAMLSerializer()
        case "MessagePack":
            return MsgPackSerializer()
        case "Avro":
            return AvroSerializer()
        case "ProtoBuf":
            return ProtoSerializer()
        case _:
            logging.error(f"Non-supported serialization format: {format}")
            exit(1)
