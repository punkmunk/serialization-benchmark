from .base import BaseSerializer

import yaml


class YAMLSerializer(BaseSerializer):
    def serialize(self, data: dict) -> bytes:
        return yaml.dump(data, Dumper=yaml.CDumper)

    def deserialize(self, data: bytes) -> dict:
        return yaml.load(data, Loader=yaml.CLoader)
