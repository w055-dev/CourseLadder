"""Модели предметной области CourseLadder."""

from typing import Any


class Discipline:
    """Учебная дисциплина."""

    def __init__(self, id: int, name: str, credits: int) -> None:
        self.id = id
        self.name = name
        self.credits = credits

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "credits": self.credits,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Discipline":
        required = ("id", "name", "credits")
        for field in required:
            if field not in data:
                raise ValueError(
                    f"В данных дисциплины отсутствует поле '{field}': {data}"
                )
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            credits=int(data["credits"]),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Discipline):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.credits == other.credits
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.credits} кредитов)"

    def __repr__(self) -> str:
        return f"Discipline(id={self.id}, name={self.name!r}, credits={self.credits})"


class Offering:
    """Учебный поток."""

    def __init__(
        self,
        id: int,
        discipline_id: int,
        teacher: str,
        total_seats: int,
        taken_seats: int = 0,
    ) -> None:
        self.id = id
        self.discipline_id = discipline_id
        self.teacher = teacher
        self.total_seats = total_seats
        self.taken_seats = taken_seats

    def free_seats(self) -> int:
        """Количество свободных мест."""
        return self.total_seats - self.taken_seats

    def add_student(self) -> None:
        """Занимает одно место."""
        self.taken_seats += 1

    def remove_student(self) -> None:
        """Освобождает одно место (не меньше нуля)."""
        if self.taken_seats > 0:
            self.taken_seats -= 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "discipline_id": self.discipline_id,
            "teacher": self.teacher,
            "total_seats": self.total_seats,
            "taken_seats": self.taken_seats,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Offering":
        required = ("id", "discipline_id", "teacher", "total_seats")
        for field in required:
            if field not in data:
                raise ValueError(
                    f"В данных потока отсутствует поле '{field}': {data}"
                )
        return cls(
            id=int(data["id"]),
            discipline_id=int(data["discipline_id"]),
            teacher=str(data["teacher"]),
            total_seats=int(data["total_seats"]),
            taken_seats=int(data.get("taken_seats", 0)),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Offering):
            return NotImplemented
        return (
            self.id == other.id
            and self.discipline_id == other.discipline_id
            and self.teacher == other.teacher
            and self.total_seats == other.total_seats
            and self.taken_seats == other.taken_seats
        )

    def __str__(self) -> str:
        return (
            f"поток #{self.id} | {self.teacher} | "
            f"свободно: {self.free_seats()}/{self.total_seats}"
        )

    def __repr__(self) -> str:
        return (
            f"Offering(id={self.id}, discipline_id={self.discipline_id}, "
            f"teacher={self.teacher!r}, total_seats={self.total_seats}, "
            f"taken_seats={self.taken_seats})"
        )


class Enrollment:
    """Запись студента на поток."""

    def __init__(self, student: str, offering_id: int) -> None:
        self.student = student
        self.offering_id = offering_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "student": self.student,
            "offering_id": self.offering_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Enrollment":
        required = ("student", "offering_id")
        for field in required:
            if field not in data:
                raise ValueError(
                    f"В данных записи отсутствует поле '{field}': {data}"
                )
        return cls(
            student=str(data["student"]),
            offering_id=int(data["offering_id"]),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Enrollment):
            return NotImplemented
        return (
            self.student == other.student
            and self.offering_id == other.offering_id
        )

    def __str__(self) -> str:
        return f"{self.student} → поток #{self.offering_id}"

    def __repr__(self) -> str:
        return f"Enrollment(student={self.student!r}, offering_id={self.offering_id})"


class Student:
    """Студент с ФИО и списком его записей."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.enrollments: list[Enrollment] = []

    def add_enrollment(self, enrollment: Enrollment) -> None:
        """Добавляет запись студенту."""
        self.enrollments.append(enrollment)

    def remove_enrollment(self, offering_id: int) -> bool:
        """Удаляет запись по id потока."""
        for index in range(len(self.enrollments)):
            if self.enrollments[index].offering_id == offering_id:
                self.enrollments.pop(index)
                return True
        return False

    def has_offering(self, offering_id: int) -> bool:
        """Проверяет, записан ли студент на поток."""
        for enrollment in self.enrollments:
            if enrollment.offering_id == offering_id:
                return True
        return False

    def __str__(self) -> str:
        return f"Студент: {self.name} (записей: {len(self.enrollments)})"
