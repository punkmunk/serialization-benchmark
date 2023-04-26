from .base import BaseSerializer

import pickle


class PickleSerializer(BaseSerializer):
    def serialize(self, data: dict) -> bytes:
        return pickle.dumps(data)

    def deserialize(self, data: bytes) -> dict:
        return pickle.loads(data)
