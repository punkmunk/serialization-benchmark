from .base import BaseSerializer

import msgpack


class MsgPackSerializer(BaseSerializer):
    def serialize(self, data: dict) -> bytes:
        return msgpack.packb(data)

    def deserialize(self, data: bytes) -> dict:
        return msgpack.unpackb(data)
