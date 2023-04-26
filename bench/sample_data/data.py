from dataclasses import asdict, dataclass
import random
import string


@dataclass
class Student:
    name: str
    surname: str
    gpa: float
    grades: dict[str, int]


@dataclass
class School:
    groups: dict[str, list[Student]]


def generate_sample_data() -> dict:
    def generate_random_string() -> str:
        return "".join(random.choices(string.ascii_letters, k=random.randint(5, 10)))

    random.seed(1337)

    student_count = 10
    subjects = [
        "Algebra",
        "Analysis",
        "Philosophy",
        "Service_Oriented_Architecture",
        "Concurrency",
        "Networks",
        "Distributed_Systems",
        "Computer_Architecture_and_Operating_Systems",
        "Functional_Programming",
        "Research_Seminar",
    ]

    return asdict(
        School(
            groups={
                f"Group_{group_number}": [
                    Student(
                        name=generate_random_string(),
                        surname=generate_random_string(),
                        gpa=random.uniform(0, 4),
                        grades={subject: random.randint(0, 10) for subject in subjects},
                    )
                    for _ in range(student_count)
                ]
                for group_number in range(1, 5)
            }
        )
    )
