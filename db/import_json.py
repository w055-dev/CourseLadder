import json
import os
import sys
from pathlib import Path

# Добавление корневой папки проекта в sys.path, чтобы Python нашел модули catalog и т.д.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Настройка окружения Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CourseLaddeR.settings")

DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> list:
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def main() -> None:
    """Основная функция импорта"""
    import django
    django.setup()

    # Импорт моделей после инициализации Django
    from catalog.models import Discipline, Student
    from offerings.models import Offering
    from enrollments.models import Enrollment

    print("Очистка старых данных...")
    Enrollment.objects.all().delete()
    Offering.objects.all().delete()
    Student.objects.all().delete()
    Discipline.objects.all().delete()

    print("Загрузка дисциплин...")
    for d in load_json("disciplines.json"):
        Discipline.objects.create(id=d["id"], name=d["name"], credits=d["credits"])

    print("Загрузка студентов...")
    enrollments = load_json("enrollments.json")
    student_names = {e["student"] for e in enrollments}
    students_map = {}
    for s_name in student_names:
        students_map[s_name] = Student.objects.create(full_name=s_name)

    print("Загрузка потоков...")
    offerings_map = {}
    for o in load_json("offerings.json"):
        disc = Discipline.objects.get(id=o["discipline_id"])
        off = Offering.objects.create(
            id=o["id"], discipline=disc, teacher=o["teacher"],
            total_seats=o["total_seats"], taken_seats=o["taken_seats"]
        )
        offerings_map[o["id"]] = off

    print("Загрузка записей...")
    for e in enrollments:
        Enrollment.objects.create(
            student=students_map[e["student"]],
            offering=offerings_map[e["offering_id"]]
        )
    print("Импорт успешно завершен через ORM!")


if __name__ == "__main__":
    main()
