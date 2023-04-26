from .base import BaseSerializer

import fastavro

import io


class AvroSerializer(BaseSerializer):
    def __init__(self) -> None:
        super().__init__()
        self.schema = fastavro.schema.load_schema("bench/serializer/avro/school.avsc")
        self.buffer = io.BytesIO()

    def serialize(self, data: dict) -> bytes:
        fastavro.schemaless_writer(self.buffer, self.schema, data)
        self.buffer.seek(0)

        return self.buffer.getvalue()

    def deserialize(self, data: bytes) -> dict:
        return fastavro.schemaless_reader(io.BytesIO(data), self.schema)
