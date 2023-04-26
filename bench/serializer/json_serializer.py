from .base import BaseSerializer

import json


class JSONSerializer(BaseSerializer):
    def serialize(self, data: dict) -> bytes:
        return json.dumps(data)

    def deserialize(self, data: bytes) -> dict:
        return json.loads(data)
