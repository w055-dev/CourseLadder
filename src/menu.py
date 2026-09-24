"""Консольный интерфейс CourseLadder."""

from src.services import (
    load_disciplines,
    load_enrollments,
    enroll_student,
    cancel_enrollment,
    find_discipline,
    find_discipline_by_id,
    sort_disciplines,
    format_disciplines,
    student_enrollments,
    total_credits,
    ServiceError,
)
from src.storage import StorageError


MENU = """
Выберите действие:
1 - Показать все дисциплины
2 - Найти дисциплину
3 - Отсортировать дисциплины
4 - Записаться на дисциплину
5 - Мои записи
6 - Отменить запись
0 - Выход
"""


def ask_int(prompt: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: нужно ввести число.")


def show_disciplines(disciplines) -> None:
    print(format_disciplines(disciplines))


def find_and_show(disciplines) -> None:
    query = input("Введите часть названия или ФИО преподавателя: ").strip()
    result = find_discipline(disciplines, query)
    if not result:
        print("Ничего не найдено.")
        return
    print(format_disciplines(result))


def sort_and_show(disciplines) -> None:
    print("Ключ сортировки: 1 - название, 2 - кредиты, 3 - свободные места")
    key_choice = ask_int("Ваш выбор: ")
    key = {1: "name", 2: "credits", 3: "free"}.get(key_choice, "name")
    reverse = input("По убыванию? (y/n): ").strip().lower() == "y"
    print(format_disciplines(sort_disciplines(disciplines, key, reverse)))


def do_enroll(student: str, disciplines, enrollments) -> None:
    show_disciplines(disciplines)
    discipline_id = ask_int("Введите ID дисциплины: ")
    try:
        enroll_student(student, discipline_id, disciplines, enrollments)
        print("Запись успешно оформлена!")
    except ServiceError as exc:
        print(f"Ошибка: {exc}")


def do_cancel(student: str, disciplines, enrollments) -> None:
    mine = student_enrollments(student, enrollments)
    if len(mine) == 0:
        print("У вас нет записей.")
        return
    for enrollment in mine:
        discipline = find_discipline_by_id(disciplines, enrollment.discipline_id)
        if discipline is not None:
            print(f"ID {discipline.id}: {discipline.name}")
    discipline_id = ask_int("Введите ID дисциплины для отмены: ")
    try:
        cancel_enrollment(student, discipline_id, disciplines, enrollments)
        print("Запись отменена.")
    except ServiceError as exc:
        print(f"Ошибка: {exc}")


def show_my(student: str, disciplines, enrollments) -> None:
    mine = student_enrollments(student, enrollments)
    if not mine:
        print("Вы пока не записаны ни на одну дисциплину.")
        return
    for e in mine:
        d = find_discipline_by_id(disciplines, e.discipline_id)
        if d is not None:
            print(f"- {d.name} | {d.teacher} | кредитов: {d.credits}")
    print(f"Всего кредитов: {total_credits(mine, disciplines)}")


def run() -> None:
    """Главный цикл программы."""
    print("===== CourseLadder: сервис выбора дисциплин =====")

    try:
        disciplines = load_disciplines()
        enrollments = load_enrollments()
    except StorageError as exc:
        print(f"Не удалось загрузить данные: {exc}")
        return

    student = input("Введите ваше ФИО: ").strip()
    if not student:
        print("Ошибка: имя не должно быть пустым.")
        return

    while True:
        print(MENU)
        action = input("Ваш выбор: ").strip()

        if action == "1":
            show_disciplines(disciplines)
        elif action == "2":
            find_and_show(disciplines)
        elif action == "3":
            sort_and_show(disciplines)
        elif action == "4":
            do_enroll(student, disciplines, enrollments)
        elif action == "5":
            show_my(student, disciplines, enrollments)
        elif action == "6":
            do_cancel(student, disciplines, enrollments)
        elif action == "0":
            print("Выход. До свидания!")
            break
        else:
            print("Ошибка: неизвестная команда.")
