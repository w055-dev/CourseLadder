"""Модели предметной области CourseLadder."""

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Discipline:
    """Учебная дисциплина."""

    id: int
    name: str
    teacher: str
    credits: int
    total_seats: int
    taken_seats: int = 0

    @property
    def free_seats(self) -> int:
        return self.total_seats - self.taken_seats

    def to_dict(self) -> dict[str, Any]:
        """Сериализация в словарь для JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Discipline":
        """Десериализация из словаря."""
        return cls(
            id=int(data["id"]),
            name=str(data["name"]),
            teacher=str(data["teacher"]),
            credits=int(data["credits"]),
            total_seats=int(data["total_seats"]),
            taken_seats=int(data.get("taken_seats", 0)),
        )


@dataclass
class Enrollment:
    """Учебный поток."""

    student: str
    discipline_id: int

    def to_dict(self) -> dict[str, Any]:
        """Сериализация в словарь для JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Enrollment":
        """Десериализация из словаря."""
        return cls(
            student=str(data["student"]),
            discipline_id=int(data["discipline_id"]),
        )
