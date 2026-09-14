import datetime

#Дисциплины: название, преподаватель, кредиты(зачетные единицы), мест всего, мест занято
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

def show_disciplines():
    print("Доступные дисциплины")
    print("-" * 100)
    for i, (name, teacher, credits, total, taken) in enumerate(disciplines, start=1):
        free = total - taken
        print(f"{i}. {name} | {teacher} | кредитов(зачетных единиц): {credits} | свободно : {free}/{total}")
    print ("-" * 100)

def main():
    print("=====Сервис выбора дисциплин=====")
    print("-" * 60)

    student_name = input("Введите ваше ФИО: ")
    if student_name == "":
        print("Ошибка: имя не должно быть пустым")
        return

    # Ввод номера дисциплины
    show_disciplines()
    choice_raw = input("Введите номер дисциплины: ")

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

    current_credits = 0

    # Проверка: не истек ли дедлайн?
    today = datetime.date.today()
    if today > deadline:
         print(f"Запись закрыта. Дедлайн был {deadline}")
         return

    # Проверка: остались ли свободные места?
    if free <= 0:
        print(f"На поток «{name}» («{teacher}») нет свободных мест")
        return

    # Проверка: превышен ли лимит кредитов?
    if current_credits + credits > max_credits:
        print("Превышен максимум кредитов(зачетных единиц) в семестре")
        return

    # Успешная запись
    print(f"Студент: {student_name}")
    print(f"Записан на {name}")
    print(f"Преподаватель: {teacher}")
    print(f"Кредитов(зачетных единиц): {credits}")
    print(f"Осталось свободных мест: {free-1}")
    print("Запись успешно оформлена!")

if __name__ == "__main__":
    main()