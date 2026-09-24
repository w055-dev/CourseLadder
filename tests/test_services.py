"""Тесты бизнес-логики CourseLadder."""

import datetime
import pytest

from src.models import Discipline, Enrollment
from src.services import (
    find_discipline,
    sort_disciplines,
    enroll_student,
    cancel_enrollment,
    total_credits,
    is_deadline_passed,
    ServiceError,
    DEADLINE
)


@pytest.fixture
def disciplines() -> list[Discipline]:
    return [
        Discipline(1, "Компьютерный дизайн", "Иванов И.И.", 5, 30, 30),
        Discipline(2, "Инструменты девопс", "Новиков С.В.", 5, 25, 10),
        Discipline(3, "Программирование ЭПиС", "Павлов И.П.", 5, 20, 19),
        Discipline(4, "Трехмерное моделирование", "Кузнецов Д.А.", 6, 15, 5),
        Discipline(5, "Машинное обучение", "Грозный И.В.", 12, 10, 1)
    ]


@pytest.fixture
def enrollments() -> list[Enrollment]:
    return []


def test_find_discipline_by_name(disciplines):
    result = find_discipline(disciplines, "дизайн")
    assert len(result) == 1
    assert result[0].id == 1


def test_find_discipline_by_teacher(disciplines):
    result = find_discipline(disciplines, "новиков")
    assert len(result) == 1
    assert result[0].id == 2


def test_find_discipline_empty_query_returns_all(disciplines):
    assert len(find_discipline(disciplines, "")) == len(disciplines)


def test_sort_by_name(disciplines):
    result = sort_disciplines(disciplines, key="name")
    assert result[0].name == "Инструменты девопс"


def test_sort_by_credits_desc(disciplines):
    result = sort_disciplines(disciplines, key="credits", reverse=True)
    assert result[0].credits == 12


def test_sort_by_free_seats(disciplines):
    result = sort_disciplines(disciplines, key="free")
    assert result[0].free_seats == 0


def test_enroll_success(disciplines, enrollments):
    enroll_student("Иванов", 2, disciplines, enrollments)
    assert len(enrollments) == 1
    assert disciplines[1].taken_seats == 11


def test_enroll_no_seats(disciplines, enrollments):
    with pytest.raises(ServiceError, match="нет свободных мест"):
        enroll_student("Иванов", 1, disciplines, enrollments)


def test_enroll_duplicate(disciplines, enrollments):
    enroll_student("Иванов", 2, disciplines, enrollments)
    with pytest.raises(ServiceError, match="уже записаны"):
        enroll_student("Иванов", 2, disciplines, enrollments)


def test_enroll_credit_limit(disciplines, enrollments):
    # 5 + 5 + 6 + 12 == 28, потом ещё + 6 = 34 > 30
    for d_id in (2, 3, 4, 5):
        enroll_student("Иванов", d_id, disciplines, enrollments)
    disciplines[0].taken_seats = 0  # освобождение места
    with pytest.raises(ServiceError, match="Превышен максимум кредитов"):
        enroll_student("Иванов", 1, disciplines, enrollments)


def test_enroll_after_deadline(disciplines, enrollments):
    after = DEADLINE + datetime.timedelta(days=1)
    with pytest.raises(ServiceError, match="Запись закрыта"):
        enroll_student("Иванов", 2, disciplines, enrollments, today=after)


def test_cancel_success(disciplines, enrollments):
    enroll_student("Иванов", 2, disciplines, enrollments)
    cancel_enrollment("Иванов", 2, disciplines, enrollments)
    assert len(enrollments) == 0
    assert disciplines[1].taken_seats == 10


def test_cancel_not_found(disciplines, enrollments):
    with pytest.raises(ServiceError, match="не найдена"):
        cancel_enrollment("Иванов", 2, disciplines, enrollments)


def test_total_credits(disciplines, enrollments):
    enroll_student("Иванов", 2, disciplines, enrollments)
    enroll_student("Иванов", 4, disciplines, enrollments)
    assert total_credits(enrollments, disciplines) == 11


def test_is_deadline_passed():
    assert is_deadline_passed(DEADLINE) is False
    assert is_deadline_passed(DEADLINE + datetime.timedelta(days=1)) is True
