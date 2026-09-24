"""Бизнес-логика CourseLadder: поиск, сортировка, бронирования."""

import datetime
from typing import Iterable

from src.models import Discipline, Enrollment
from src.storage import load_json, save_json


DISCIPLINES_PATH = "data/disciplines.json"
ENROLLMENTS_PATH = "data/enrollments.json"
DEADLINE = datetime.date(2026, 12, 21)
MAX_CREDITS = 30


class ServiceError(Exception):
    """Ошибка бизнес-логики."""

# Загрузки/сохранения дисциплин/потоков


def load_disciplines() -> list[Discipline]:
    raw = load_json(DISCIPLINES_PATH)
    result = []
    for i in raw:
        result.append(Discipline.from_dict(i))
    return result


def save_disciplines(disciplines: list[Discipline]) -> None:
    raw = []
    for d in disciplines:
        raw.append(d.to_dict())
    save_json(DISCIPLINES_PATH, raw)


def load_enrollments() -> list[Enrollment]:
    raw = load_json(ENROLLMENTS_PATH)
    result = []
    for i in raw:
        result.append(Enrollment.from_dict(i))
    return result


def save_enrollments(enrollments: list[Enrollment]) -> None:
    raw = []
    for e in enrollments:
        raw.append(e.to_dict())
    save_json(ENROLLMENTS_PATH, raw)


# Обрабатывание коллекций

def find_discipline(disciplines: Iterable[Discipline], query: str) -> list[Discipline]:
    """Поиск дисциплин по подстроке в названии или преподавателе."""
    q = query.strip().lower()
    if q == "":
        return list(disciplines)
    result = []
    for discipline in disciplines:
        name_match = q in discipline.name.lower()
        teacher_match = q in discipline.teacher.lower()
        if name_match or teacher_match:
            result.append(discipline)
    return result


def sort_disciplines(
    disciplines: Iterable[Discipline],
    key: str = "name",
    reverse: bool = False,
) -> list[Discipline]:
    """Сортировка дисциплин по названию, кредитам или свободным местам."""
    if key == "credits":
        return sorted(disciplines, key=lambda d: d.credits, reverse=reverse)
    if key == "free":
        return sorted(disciplines, key=lambda d: d.free_seats, reverse=reverse)
    return sorted(disciplines, key=lambda d: d.name.lower(), reverse=reverse)


def format_disciplines(disciplines: Iterable[Discipline]) -> str:
    """Формирует текстовый вывод списка дисциплин."""
    lines = ["Список дисциплин:", "-" * 80]
    for i, d in enumerate(disciplines, start=1):
        lines.append(
            f"{i}. {d.name} | {d.teacher} | "
            f"кредитов: {d.credits} | свободно: {d.free_seats}/{d.total_seats}"
        )
    lines.append("-" * 80)
    return "\n".join(lines)


# Проверки

def is_deadline_passed(today: datetime.date | None = None) -> bool:
    if today is None:  # случай, когда дата не передана
        today = datetime.date.today()
    return today > DEADLINE


def total_credits(enrollments: Iterable[Enrollment],
                  disciplines: Iterable[Discipline]) -> int:
    total = 0
    for enrollment in enrollments:
        for discipline in disciplines:
            if discipline.id == enrollment.discipline_id:
                total += discipline.credits
                break
    return total


def find_discipline_by_id(
    disciplines: list[Discipline],
    discipline_id: int,
) -> Discipline | None:
    """Возвращает дисциплину по id или None."""
    for discipline in disciplines:
        if discipline.id == discipline_id:
            return discipline
    return None


def find_enrollment_index(
    enrollments: list[Enrollment],
    student: str,
    discipline_id: int,
) -> int:
    """Возвращает индекс записи или -1, если её нет."""
    for index in range(len(enrollments)):
        enrollment = enrollments[index]
        if (enrollment.student == student
                and enrollment.discipline_id == discipline_id):
            return index
    return -1


def is_already_enrolled(
    enrollments: list[Enrollment],
    student: str,
    discipline_id: int,
) -> bool:
    """Проверяет, записан ли студент уже на эту дисциплину."""
    return find_enrollment_index(enrollments, student, discipline_id) != -1


def student_credits(
    enrollments: list[Enrollment],
    disciplines: list[Discipline],
    student: str,
) -> int:
    """Считает кредиты(зачетные единицы), которые уже набрал конкретный студент."""
    mine = student_enrollments(student, enrollments)
    return total_credits(mine, disciplines)

# Записи


def enroll_student(
    student: str,
    discipline_id: int,
    disciplines: list[Discipline],
    enrollments: list[Enrollment],
    today: datetime.date | None = None,
) -> None:
    """Записывает студента на дисциплину с проверкой всех правил."""
    if not student.strip():
        raise ServiceError("ФИО не может быть пустым")

    discipline = find_discipline_by_id(disciplines, discipline_id)
    if discipline is None:
        raise ServiceError("Дисциплина не найдена")

    if is_deadline_passed(today):
        raise ServiceError(f"Запись закрыта. Дедлайн был {DEADLINE}")

    if is_already_enrolled(enrollments, student, discipline_id):
        raise ServiceError("Вы уже записаны на эту дисциплину")

    if discipline.free_seats <= 0:
        raise ServiceError(f"На поток «{discipline.name}» нет свободных мест")

    current = student_credits(enrollments, disciplines, student)
    if current + discipline.credits > MAX_CREDITS:
        raise ServiceError(
            f"Превышен максимум кредитов: {current + discipline.credits} "
            f"из {MAX_CREDITS}"
        )

    enrollments.append(Enrollment(student=student, discipline_id=discipline_id))
    discipline.taken_seats += 1

    save_disciplines(disciplines)
    save_enrollments(enrollments)


def cancel_enrollment(
    student: str,
    discipline_id: int,
    disciplines: list[Discipline],
    enrollments: list[Enrollment],
    today: datetime.date | None = None,
) -> None:
    """Отменяет запись студента на дисциплину."""
    if is_deadline_passed(today):
        raise ServiceError(f"Отмена недоступна: запись закрыта {DEADLINE}")

    index = find_enrollment_index(enrollments, student, discipline_id)
    if index == -1:
        raise ServiceError("Запись не найдена")

    enrollments.pop(index)

    discipline = find_discipline_by_id(disciplines, discipline_id)
    if discipline is not None and discipline.taken_seats > 0:
        discipline.taken_seats -= 1

    save_disciplines(disciplines)
    save_enrollments(enrollments)


def student_enrollments(
    student: str,
    enrollments: Iterable[Enrollment],
) -> list[Enrollment]:
    return [e for e in enrollments if e.student == student]
