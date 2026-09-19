import datetime

# Дисциплины: название, преподаватель, кредиты(зачетные единицы), мест всего, мест занято
disciplines = [
    ("Компьютерный дизайн", "Иванов И.И.", 5, 30, 30),
    ("Инструменты девопс", "Новиков С.В.", 5, 25, 10),
    ("Программирование электронных приборов и систем", "Павлов И.П.", 5, 20, 19),
    ("Трехмерное моделирование индустриальных объектов", "Кузнецов Д.А.", 6, 15, 5),
]

# Пробный дедлайн на 21 сентября 2026 года
deadline = datetime.date(2026, 9, 21)

# Максимум кредитов(зачетных единиц) в семестре
max_credits = 30
my_enrollments: list[int] = []


def show_disciplines():
    print("Доступные дисциплины")
    print("-" * 100)
    for i, (name, teacher, credits, total, taken) in enumerate(disciplines, start=1):
        free = total - taken
        print(f"{i}. {name} | {teacher} | кредитов(зачетных единиц): {credits} | свободно : {free}/{total}")
    print("-" * 100)


def show_my_enrollments():
    print("Мои записи")
    print("-" * 60)

    if len(my_enrollments) == 0:
        print("Вы еще не записаны ни на одну дисциплину. ")
        print("-" * 60)
        return

    total_credits = 0
    for indx in my_enrollments:
        name, teacher, credits, total, taken = disciplines[indx]
        total_credits += credits
        print(f"- {name} | {teacher} | кредитов: {credits}")

    print("-" * 60)
    print(f"Всего кредитов: {total_credits} из {max_credits}")
    print("-" * 60)


def enroll(student_name):
    # Ввод номера дисциплины
    show_disciplines()
    choice_raw = input("Введите номер дисциплины: ").strip()

    # Проверка с преобразованием типов
    if not choice_raw.isdigit():
        print("Ошибка: нужно ввести число.")
        return

    choice = int(choice_raw)
    if choice < 1 or choice > len(disciplines):
        print("Ошибка: такого номера нет в списке дисциплин")
        return

    # Выбранная дисциплина:
    name, teacher, credits, total, taken = disciplines[choice - 1]
    free = total - taken

    # Проверка: нет ли дублирования?
    if (choice - 1) in my_enrollments:
        print(f"Вы уже записаны на курс «{name}».")
        return

    # Проверка: не истек ли дедлайн?
    today = datetime.date.today()
    if today > deadline:
        print(f"Запись закрыта. Дедлайн был {deadline}")
        return

    # Проверка: остались ли свободные места?
    if free <= 0:
        print(f"На поток «{name}» («{teacher}») нет свободных мест")
        return

    current_credits = 0
    for i in my_enrollments:
        current_credits += disciplines[i][2]

    # Проверка: превышен ли лимит кредитов?
    if current_credits + credits > max_credits:
        print(f"Превышен максимум кредитов. Сейчас у вас {current_credits}, "
              f"а с этой дисциплиной будет {current_credits + credits} из {max_credits}.")
        return

    my_enrollments.append(choice - 1)
    d_name, d_teacher, d_credits, d_total, d_taken = disciplines[choice - 1]
    disciplines[choice - 1] = (d_name, d_teacher, d_credits, d_total, d_taken + 1)

    # Успешная запись
    print(f"\nСтудент: {student_name}")
    print(f"Записан на {name}")
    print(f"Преподаватель: {teacher}")
    print(f"Кредитов(зачетных единиц): {credits}")
    print(f"Осталось свободных мест: {free - 1}")
    print("Запись успешно оформлена!")


def cancel_enrollment():
    if len(my_enrollments) == 0:
        print("У вас нет записей для отмены.")
        return

    show_my_enrollments()
    choice_raw = input("Введите номер дисциплины для отмены (1-" + str(len(my_enrollments)) + "): ").strip()

    if not choice_raw.isdigit():
        print("Ошибка: нужно ввести число.")
        return

    pos = int(choice_raw)
    if pos < 1 or pos > len(my_enrollments):
        print("Ошибка: такого номера нет в списке ваших записей.")
        return

    # Проверка дедлайна
    today = datetime.date.today()
    if today > deadline:
        print(f"Отмена недоступна: запись закрыта {deadline}.")
        return

    index = my_enrollments[pos - 1]
    name, teacher, credits, total, taken = disciplines[index]

    # Убираем из списка и возвращаем место
    my_enrollments.pop(pos - 1)
    disciplines[index] = (name, teacher, credits, total, taken - 1)

    print(f"Запись на «{name}» отменена. Освободилось место.")


def main():
    print("===== Сервис выбора дисциплин =====")
    print("-" * 60)

    student_name = input("Введите ваше ФИО: ").strip()
    if student_name == "":
        print("Ошибка: имя не должно быть пустым")
        return

    # Меню действий
    while True:
        print("\nВыберите действие:")
        print("1 - Показать список дисциплин")
        print("2 - Записаться на дисциплину")
        print("3 - Мои записи")
        print("4 - Отменить запись")
        print("0 - Выход")

        action = input("Ваш выбор: ").strip()

        if action == "1":
            show_disciplines()
        elif action == "2":
            enroll(student_name)
        elif action == "3":
            show_my_enrollments()
        elif action == "4":
            cancel_enrollment()
        elif action == "0":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Ошибка: неизвестная команда. Введите число от 0 до 4.")


if __name__ == "__main__":
    main()