"""Консольный интерфейс CourseLadder."""

from src.models import Discipline, Offering, Student
from src.services import CourseService, ServiceError
from src.storage import StorageError


MENU = """
Выберите действие:
1 - Показать каталог дисциплин
2 - Найти дисциплину
3 - Показать потоки
4 - Отсортировать потоки
5 - Записаться на поток
6 - Мои записи
7 - Отменить запись
0 - Выход
"""

SORT_KEYS = {
    1: "name",
    2: "credits",
    3: "free",
}


def ask_int(prompt: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: нужно ввести число.")


def show_disciplines(disciplines: list[Discipline]) -> None:
    """Печатает каталог дисциплин."""
    print("Каталог дисциплин:")
    print("-" * 80)
    if len(disciplines) == 0:
        print("(пусто)")
    else:
        for discipline in disciplines:
            print(f"ID {discipline.id}: {discipline}")
    print("-" * 80)


def show_offerings(offerings: list[Offering], service: CourseService,) -> None:
    """Печатает потоки с названиями дисциплин."""
    print("Потоки:")
    print("-" * 80)
    if len(offerings) == 0:
        print("(пусто)")
    else:
        for offering in offerings:
            discipline = service.find_discipline_by_id(
                offering.discipline_id
            )
            name = discipline.name if discipline else "?"
            credits = discipline.credits if discipline else 0
            print(
                f"ID {offering.id}: {name} | {offering.teacher} | "
                f"кредитов: {credits} | "
                f"свободно: {offering.free_seats()}/{offering.total_seats}"
            )
    print("-" * 80)


def show_catalog(service: CourseService) -> None:
    """Печатает каталог дисциплин."""
    show_disciplines(service.disciplines)


def show_all_offerings(service: CourseService) -> None:
    """Печатает все потоки."""
    show_offerings(service.offerings, service)


def find_and_show(service: CourseService) -> None:
    """Ищет дисциплины и печатает их."""
    query = input("Введите часть названия дисциплины: ").strip()
    result = service.find(query)
    if len(result) == 0:
        print("Ничего не найдено.")
        return
    show_disciplines(result)


def sort_and_show(service: CourseService) -> None:
    """Сортирует потоки и печатает их."""
    print("Ключ сортировки: 1 - название, 2 - кредиты, 3 - свободные места")
    key_choice = ask_int("Ваш выбор: ")
    key = SORT_KEYS.get(key_choice, "name")

    answer = input("По убыванию? (y/n): ").strip().lower()
    reverse = (answer == "y")

    sorted_list = service.sort_offerings(key, reverse)
    show_offerings(sorted_list, service)


def do_enroll(service: CourseService, student: Student) -> None:
    """Записывает студента на поток."""
    show_offerings(service.offerings, service)
    offering_id = ask_int("Введите ID потока: ")
    try:
        service.enroll(student, offering_id)
        print("Запись успешно оформлена!")
    except ServiceError as exc:
        print(f"Ошибка: {exc}")


def do_cancel(service: CourseService, student: Student) -> None:
    """Отменяет запись студента на поток."""
    mine = service.student_enrollments(student)
    if len(mine) == 0:
        print("У вас нет записей.")
        return
    for enrollment in mine:
        offering = service.find_offering_by_id(enrollment.offering_id)
        if offering is not None:
            discipline = service.find_discipline_by_id(
                offering.discipline_id
            )
            name = discipline.name if discipline else "?"
            print(
                f"ID {offering.id}: {name} | {offering.teacher}"
            )

    offering_id = ask_int("Введите ID потока для отмены: ")
    try:
        service.cancel(student, offering_id)
        print("Запись отменена.")
    except ServiceError as exc:
        print(f"Ошибка: {exc}")


def show_my(service: CourseService, student: Student) -> None:
    """Показывает записи текущего студента."""
    mine = service.student_enrollments(student)
    if len(mine) == 0:
        print("Вы пока не записаны ни на один поток.")
        return

    for enrollment in mine:
        offering = service.find_offering_by_id(enrollment.offering_id)
        if offering is None:
            continue
        discipline = service.find_discipline_by_id(
            offering.discipline_id
        )
        if discipline is not None:
            print(
                f"- {discipline.name} | {offering.teacher} | "
                f"кредитов: {discipline.credits}"
            )

    print(f"Всего кредитов: {service.total_credits(mine)}")


def run() -> None:
    """Главный цикл программы."""
    print("===== CourseLadder: сервис выбора дисциплин =====")

    service = CourseService()
    try:
        service.load()
    except StorageError as exc:
        print(f"Не удалось загрузить данные: {exc}")
        return

    name = input("Введите ваше ФИО: ").strip()
    if name == "":
        print("Ошибка: имя не должно быть пустым.")
        return

    student = Student(name)

    while True:
        print(MENU)
        action = input("Ваш выбор: ").strip()

        if action == "1":
            show_catalog(service)
        elif action == "2":
            find_and_show(service)
        elif action == "3":
            show_all_offerings(service)
        elif action == "4":
            sort_and_show(service)
        elif action == "5":
            do_enroll(service, student)
        elif action == "6":
            show_my(service, student)
        elif action == "7":
            do_cancel(service, student)
        elif action == "0":
            print("Выход. До свидания!")
            break
        else:
            print("Ошибка: неизвестная команда.")
