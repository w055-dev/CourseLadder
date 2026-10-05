"""Бизнес-логика CourseLadder в виде класса CourseService."""

import datetime
from typing import Iterable

from src.models import Discipline, Enrollment, Offering, Student
from src.storage import load_json, save_json


class ServiceError(Exception):
    """Ошибка бизнес-логики."""


class CourseService:
    """Сервис выбора дисциплин."""

    DISCIPLINES_PATH = "data/disciplines.json"
    OFFERINGS_PATH = "data/offerings.json"
    ENROLLMENTS_PATH = "data/enrollments.json"
    DEADLINE = datetime.date(2026, 12, 21)
    MAX_CREDITS = 30

    def __init__(self) -> None:
        self.disciplines: list[Discipline] = []
        self.offerings: list[Offering] = []
        self.enrollments: list[Enrollment] = []

    def load(self) -> None:
        """Загружает дисциплины, потоки и записи из JSON-файлов."""
        raw_d = load_json(self.DISCIPLINES_PATH)
        self.disciplines = [Discipline.from_dict(d) for d in raw_d]

        raw_o = load_json(self.OFFERINGS_PATH)
        self.offerings = [Offering.from_dict(o) for o in raw_o]

        raw_e = load_json(self.ENROLLMENTS_PATH)
        self.enrollments = [Enrollment.from_dict(e) for e in raw_e]

    def save(self) -> None:
        """Сохраняет дисциплины, потоки и записи в JSON-файлы."""
        save_json(
            self.DISCIPLINES_PATH,
            [d.to_dict() for d in self.disciplines],
        )
        save_json(
            self.OFFERINGS_PATH,
            [o.to_dict() for o in self.offerings],
        )
        save_json(
            self.ENROLLMENTS_PATH,
            [e.to_dict() for e in self.enrollments],
        )

    def find_discipline_by_id(self, discipline_id: int) -> Discipline | None:
        """Возвращает дисциплину по id или None."""
        for discipline in self.disciplines:
            if discipline.id == discipline_id:
                return discipline
        return None

    def find_offering_by_id(self, offering_id: int) -> Offering | None:
        """Возвращает поток по id или None."""
        for offering in self.offerings:
            if offering.id == offering_id:
                return offering
        return None

    def find(self, query: str) -> list[Discipline]:
        """Поиск дисциплин по подстроке в названии."""
        q = query.strip().lower()
        if q == "":
            return list(self.disciplines)

        result = []
        for discipline in self.disciplines:
            if q in discipline.name.lower():
                result.append(discipline)
        return result

    def find_offerings(self, query: str) -> list[Offering]:
        """Поиск потоков по подстроке в названии дисциплины или ФИО преподавателя."""
        q = query.strip().lower()
        if q == "":
            return list(self.offerings)

        result = []
        for offering in self.offerings:
            discipline = self.find_discipline_by_id(offering.discipline_id)
            name = discipline.name.lower() if discipline else ""
            teacher = offering.teacher.lower()
            if q in name or q in teacher:
                result.append(offering)
        return result

    def sort_offerings(self, key: str = "name", reverse: bool = False) -> list[Offering]:
        """Сортировка потоков по названию дисциплины, кредитам или свободным местам."""
        if key == "credits":
            return sorted(
                self.offerings,
                key=lambda o: self._credits_of(o),
                reverse=reverse,
            )
        if key == "free":
            return sorted(
                self.offerings,
                key=lambda o: o.free_seats(),
                reverse=reverse,
            )
        return sorted(
            self.offerings,
            key=lambda o: self._name_of(o),
            reverse=reverse,
        )

    def _name_of(self, offering: Offering) -> str:
        """Название дисциплины потока в нижнем регистре (для сортировки)."""
        discipline = self.find_discipline_by_id(offering.discipline_id)
        return discipline.name.lower() if discipline else ""

    def _credits_of(self, offering: Offering) -> int:
        """Кредиты дисциплины потока."""
        discipline = self.find_discipline_by_id(offering.discipline_id)
        return discipline.credits if discipline else 0

    def is_deadline_passed(self, today: datetime.date | None = None) -> bool:
        """Проверяет, истёк ли срок записи."""
        if today is None:
            today = datetime.date.today()
        return today > self.DEADLINE

    def student_enrollments(self, student: Student) -> list[Enrollment]:
        """Возвращает записи конкретного студента."""
        result = []
        for enrollment in self.enrollments:
            if enrollment.student == student.name:
                result.append(enrollment)
        return result

    def total_credits(self, enrollments: Iterable[Enrollment]) -> int:
        """Считает сумму кредитов по переданным записям."""
        total = 0
        for enrollment in enrollments:
            offering = self.find_offering_by_id(enrollment.offering_id)
            if offering is None:
                continue
            discipline = self.find_discipline_by_id(offering.discipline_id)
            if discipline is not None:
                total += discipline.credits
        return total

    def student_credits(self, student: Student) -> int:
        """Кредиты, которые уже набрал студент."""
        mine = self.student_enrollments(student)
        return self.total_credits(mine)

    def enroll(self, student: Student, offering_id: int, today: datetime.date | None = None) -> None:
        """Записывает студента на поток с проверкой всех правил."""
        if student.name.strip() == "":
            raise ServiceError("ФИО не может быть пустым")

        offering = self.find_offering_by_id(offering_id)
        if offering is None:
            raise ServiceError("Поток не найден")

        discipline = self.find_discipline_by_id(offering.discipline_id)
        if discipline is None:
            raise ServiceError("Дисциплина потока не найдена")

        if self.is_deadline_passed(today):
            raise ServiceError(
                f"Запись закрыта. Дедлайн был {self.DEADLINE}"
            )

        if student.has_offering(offering_id):
            raise ServiceError("Вы уже записаны на этот поток")

        if offering.free_seats() <= 0:
            raise ServiceError(
                f"На поток «{discipline.name}» ({offering.teacher}) "
                f"нет свободных мест"
            )

        current = self.student_credits(student)
        new_total = current + discipline.credits
        if new_total > self.MAX_CREDITS:
            raise ServiceError(
                f"Превышен максимум кредитов: {new_total} "
                f"из {self.MAX_CREDITS}"
            )

        enrollment = Enrollment(
            student=student.name, offering_id=offering_id
        )
        self.enrollments.append(enrollment)
        student.add_enrollment(enrollment)
        offering.add_student()

        self.save()

    def cancel(self, student: Student, offering_id: int, today: datetime.date | None = None) -> None:
        """Отменяет запись студента на поток."""
        if self.is_deadline_passed(today):
            raise ServiceError(
                f"Отмена недоступна: запись закрыта {self.DEADLINE}"
            )

        if not student.has_offering(offering_id):
            raise ServiceError("Запись не найдена")

        student.remove_enrollment(offering_id)

        for index in range(len(self.enrollments)):
            e = self.enrollments[index]
            if (e.student == student.name
                    and e.offering_id == offering_id):
                self.enrollments.pop(index)
                break

        offering = self.find_offering_by_id(offering_id)
        if offering is not None:
            offering.remove_student()

        self.save()
