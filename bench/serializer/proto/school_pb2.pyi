from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class School(_message.Message):
    __slots__ = ["groups"]
    class GroupsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Students
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Students, _Mapping]] = ...) -> None: ...
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.MessageMap[str, Students]
    def __init__(self, groups: _Optional[_Mapping[str, Students]] = ...) -> None: ...

class Student(_message.Message):
    __slots__ = ["gpa", "grades", "name", "surname"]
    class GradesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    GPA_FIELD_NUMBER: _ClassVar[int]
    GRADES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURNAME_FIELD_NUMBER: _ClassVar[int]
    gpa: float
    grades: _containers.ScalarMap[str, int]
    name: str
    surname: str
    def __init__(self, name: _Optional[str] = ..., surname: _Optional[str] = ..., gpa: _Optional[float] = ..., grades: _Optional[_Mapping[str, int]] = ...) -> None: ...

class Students(_message.Message):
    __slots__ = ["students"]
    STUDENTS_FIELD_NUMBER: _ClassVar[int]
    students: _containers.RepeatedCompositeFieldContainer[Student]
    def __init__(self, students: _Optional[_Iterable[_Union[Student, _Mapping]]] = ...) -> None: ...
