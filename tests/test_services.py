"""Тесты бизнес-логики CourseLadder."""

import datetime
import pytest

from src.models import Discipline, Offering, Student
from src.services import CourseService, ServiceError


@pytest.fixture
def service() -> CourseService:
    s = CourseService()
    s.disciplines = [
        Discipline(1, "Компьютерный дизайн", 5),
        Discipline(2, "Инструменты девопс", 5),
        Discipline(3, "Программирование ЭПиС", 5),
        Discipline(4, "Трехмерное моделирование", 6),
        Discipline(5, "Машинное обучение", 11),
    ]
    s.offerings = [
        Offering(1, 1, "Иванов И.И.", 30, 30),
        Offering(2, 2, "Новиков С.В.", 25, 10),
        Offering(3, 3, "Павлов И.П.", 20, 19),
        Offering(4, 4, "Кузнецов Д.А.", 15, 5),
        Offering(5, 5, "Смирнов А.А.", 10, 0),
    ]
    s.enrollments = []
    return s


@pytest.fixture
def student() -> Student:
    return Student("Иванов")


def test_find_discipline_by_id_exists(service):
    d = service.find_discipline_by_id(2)
    assert d is not None
    assert d.name == "Инструменты девопс"


def test_find_discipline_by_id_missing(service):
    assert service.find_discipline_by_id(99) is None


def test_find_offering_by_id_exists(service):
    o = service.find_offering_by_id(2)
    assert o is not None
    assert o.teacher == "Новиков С.В."


def test_find_offering_by_id_missing(service):
    assert service.find_offering_by_id(99) is None


def test_find_discipline_by_name(service):
    result = service.find("дизайн")
    assert len(result) == 1
    assert result[0].id == 1


def test_find_discipline_empty_returns_all(service):
    assert len(service.find("")) == len(service.disciplines)


def test_find_offerings_by_teacher(service):
    result = service.find_offerings("новиков")
    assert len(result) == 1
    assert result[0].id == 2


def test_find_offerings_by_discipline_name(service):
    result = service.find_offerings("дизайн")
    assert len(result) == 1
    assert result[0].id == 1


def test_sort_offerings_by_name(service):
    result = service.sort_offerings(key="name")
    assert result[0].id == 2  # Инструменты девопс


def test_sort_offerings_by_credits_desc(service):
    result = service.sort_offerings(key="credits", reverse=True)
    assert result[0].id == 5  # Машинное обучение, 11 кредитов


def test_sort_offerings_by_free(service):
    result = service.sort_offerings(key="free")
    assert result[0].free_seats() == 0


def test_enroll_success(service, student):
    service.enroll(student, 2)
    assert len(service.enrollments) == 1
    assert service.find_offering_by_id(2).taken_seats == 11
    assert student.has_offering(2) is True


def test_enroll_no_seats(service, student):
    with pytest.raises(ServiceError, match="нет свободных мест"):
        service.enroll(student, 1)


def test_enroll_duplicate(service, student):
    service.enroll(student, 2)
    with pytest.raises(ServiceError, match="уже записаны"):
        service.enroll(student, 2)


def test_enroll_credit_limit(service, student):
    # 5 + 5 + 6 + 11 = 27, потом + 5 = 32 > 30
    for offering_id in (2, 3, 4, 5):
        service.enroll(student, offering_id)
    service.find_offering_by_id(1).taken_seats = 0
    with pytest.raises(ServiceError, match="Превышен максимум кредитов"):
        service.enroll(student, 1)


def test_enroll_after_deadline(service, student):
    after = CourseService.DEADLINE + datetime.timedelta(days=1)
    with pytest.raises(ServiceError, match="Запись закрыта"):
        service.enroll(student, 2, today=after)


def test_enroll_empty_name(service):
    empty = Student("")
    with pytest.raises(ServiceError, match="ФИО не может быть пустым"):
        service.enroll(empty, 2)


def test_enroll_offering_not_found(service, student):
    with pytest.raises(ServiceError, match="Поток не найден"):
        service.enroll(student, 99)


def test_cancel_success(service, student):
    service.enroll(student, 2)
    service.cancel(student, 2)
    assert len(service.enrollments) == 0
    assert service.find_offering_by_id(2).taken_seats == 10
    assert student.has_offering(2) is False


def test_cancel_not_found(service, student):
    with pytest.raises(ServiceError, match="Запись не найдена"):
        service.cancel(student, 2)


def test_cancel_after_deadline(service, student):
    service.enroll(student, 2)
    after = CourseService.DEADLINE + datetime.timedelta(days=1)
    with pytest.raises(ServiceError, match="Отмена недоступна"):
        service.cancel(student, 2, today=after)


def test_total_credits(service, student):
    service.enroll(student, 2)
    service.enroll(student, 4)
    mine = service.student_enrollments(student)
    assert service.total_credits(mine) == 11


def test_is_deadline_passed():
    s = CourseService()
    assert s.is_deadline_passed(CourseService.DEADLINE) is False
    after = CourseService.DEADLINE + datetime.timedelta(days=1)
    assert s.is_deadline_passed(after) is True
