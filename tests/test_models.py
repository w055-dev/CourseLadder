"""Тесты моделей CourseLadder."""

from src.models import Discipline, Enrollment, Offering, Student


def test_discipline_to_from_dict():
    d = Discipline(1, "Test", 5)
    assert Discipline.from_dict(d.to_dict()) == d


def test_discipline_str():
    d = Discipline(1, "Test", 5)
    assert "Test" in str(d)
    assert "5" in str(d)


def test_offering_free_seats():
    o = Offering(1, 1, "Teacher", 30, 10)
    assert o.free_seats() == 20


def test_offering_add_and_remove_student():
    o = Offering(1, 1, "Teacher", 30, 10)
    o.add_student()
    assert o.taken_seats == 11
    o.remove_student()
    assert o.taken_seats == 10


def test_offering_remove_not_below_zero():
    o = Offering(1, 1, "Teacher", 30, 0)
    o.remove_student()
    assert o.taken_seats == 0


def test_offering_to_from_dict():
    o = Offering(1, 1, "Teacher", 30, 10)
    assert Offering.from_dict(o.to_dict()) == o


def test_offering_str():
    o = Offering(1, 1, "Teacher", 30, 10)
    assert "Teacher" in str(o)


def test_enrollment_to_from_dict():
    e = Enrollment("Иванов", 2)
    assert Enrollment.from_dict(e.to_dict()) == e


def test_student_add_and_remove_enrollment():
    s = Student("Иванов")
    e = Enrollment("Иванов", 2)
    s.add_enrollment(e)
    assert len(s.enrollments) == 1
    assert s.remove_enrollment(2) is True
    assert len(s.enrollments) == 0


def test_student_has_offering():
    s = Student("Иванов")
    s.add_enrollment(Enrollment("Иванов", 2))
    assert s.has_offering(2) is True
    assert s.has_offering(3) is False


def test_student_str():
    s = Student("Иванов")
    assert "Иванов" in str(s)
