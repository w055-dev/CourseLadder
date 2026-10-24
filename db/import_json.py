import json
from pathlib import Path
from db.database import get_connection, init_db

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> list:
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def import_data() -> None:
    init_db()
    disciplines = load_json("disciplines.json")
    offerings = load_json("offerings.json")
    enrollments = load_json("enrollments.json")
    students = {e["student"] for e in enrollments}

    with get_connection() as conn:
        # Дисциплины
        for d in disciplines:
            conn.execute("INSERT INTO discipline (id, name, credits) VALUES (?, ?, ?)",
                         (d["id"], d["name"], d["credits"]))
        
        # Студенты
        student_ids = {}
        for s_name in students:
            cursor = conn.execute("INSERT INTO student (full_name) VALUES (?)", (s_name,))
            student_ids[s_name] = cursor.lastrowid

        # Потоки
        for o in offerings:
            conn.execute("INSERT INTO offering (id, discipline_id, teacher, total_seats, taken_seats) "
                         "VALUES (?, ?, ?, ?, ?)",
                         (o["id"], o["discipline_id"], o["teacher"], o["total_seats"], o["taken_seats"]))

        # Записи
        for e in enrollments:
            sid = student_ids[e["student"]]
            conn.execute("INSERT INTO enrollment (student_id, offering_id) VALUES (?, ?)",
                         (sid, e["offering_id"]))
        conn.commit()
        print("Импорт успешно завершен!")


if __name__ == "__main__":
    import_data()
