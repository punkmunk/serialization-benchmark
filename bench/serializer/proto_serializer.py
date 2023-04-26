from .base import BaseSerializer
from .proto import school_pb2


class ProtoSerializer(BaseSerializer):
    @staticmethod
    def prepare_data(data: dict) -> school_pb2.School:
        return school_pb2.School(
            groups={
                group: school_pb2.Students(
                    students=[
                        school_pb2.Student(
                            name=student["name"],
                            surname=student["surname"],
                            gpa=student["gpa"],
                            grades=student["grades"],
                        )
                        for student in students
                    ]
                )
                for group, students in data["groups"].items()
            }
        )

    def serialize(self, data: school_pb2.School) -> bytes:
        return data.SerializeToString()

    def deserialize(self, data: bytes) -> school_pb2.School:
        school = school_pb2.School()
        school.ParseFromString(data)

        return school
