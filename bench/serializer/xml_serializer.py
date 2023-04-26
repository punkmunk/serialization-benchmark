from .base import BaseSerializer

import dicttoxml
import xmltodict


class XMLSerializer(BaseSerializer):
    @staticmethod
    def prepare_data(data: dict) -> dict:
        return xmltodict.parse(dicttoxml.dicttoxml(data))

    def serialize(self, data: dict) -> bytes:
        return xmltodict.unparse(data)

    def deserialize(self, data: bytes) -> dict:
        return xmltodict.parse(data)
