from abc import abstractmethod


class BaseSerializer:
    @staticmethod
    def prepare_data(data: dict) -> dict:
        return data

    @abstractmethod
    def serialize(self, data: dict) -> bytes:
        ...

    @abstractmethod
    def deserialize(self, data: bytes) -> dict:
        ...
