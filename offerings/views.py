import sqlite3
from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from db.database import get_connection


def offering_list(request: HttpRequest) -> HttpResponse:
    with get_connection() as conn:
        # JOIN: данные потока и его дисциплины
        offerings = conn.execute("""
        SELECT o.id, o.teacher, o.total_seats, o.taken_seats,
            (o.total_seats - o.taken_seats) AS free_seats,
            d.id AS discipline_id, d.name AS discipline_name, d.credits
        FROM offering o
        JOIN discipline d ON o.discipline_id = d.id
    """).fetchall()
    return render(request, "offerings/offering_list.html", {"offerings": offerings})


def offering_detail2(request: HttpRequest, offering_id: int) -> HttpResponse:
    with get_connection() as conn:
        offering = conn.execute("""
            SELECT o.*, 
                   d.name AS discipline_name, 
                   d.credits,
                   (o.total_seats - o.taken_seats) AS free_seats
            FROM offering o 
            JOIN discipline d ON o.discipline_id = d.id
            WHERE o.id = ?
        """, (offering_id,)).fetchone()
        if not offering:
            raise Http404("Поток не найден")
    return render(request, "offerings/offering_detail.html", {"offering": offering})


def enroll(request: HttpRequest, offering_id: int) -> HttpResponse:
    student_name = request.GET.get("student", "").strip()
    error_message = ""
    success = False

    with get_connection() as conn:
        offering = conn.execute("""
            SELECT o.*, d.credits AS d_credits, d.name AS d_name 
            FROM offering o JOIN discipline d ON o.discipline_id = d.id
            WHERE o.id = ?
        """, (offering_id,)).fetchone()
        if not offering:
            raise Http404("Поток не найден")

        if student_name:
            # 1. Ищем или создаем студента
            student = conn.execute("SELECT * FROM student WHERE full_name = ?", (student_name,)).fetchone()
            if not student:
                cursor = conn.execute("INSERT INTO student (full_name) VALUES (?)", (student_name,))
                conn.commit()
                student_id, max_credits, current_credits = cursor.lastrowid, 30, 0
            else:
                student_id, max_credits = student["id"], student["max_credits"]
                # 2. Агрегатный запрос: сколько кредитов уже набрано
                current_credits = conn.execute("""
                    SELECT COALESCE(SUM(d.credits), 0) AS total
                    FROM enrollment e
                    JOIN offering o ON e.offering_id = o.id
                    JOIN discipline d ON o.discipline_id = d.id
                    WHERE e.student_id = ?
                """, (student_id,)).fetchone()["total"]

            # 3. Проверка лимита
            if current_credits + offering["d_credits"] > max_credits:
                error_message = f"Превышен лимит кредитов: {current_credits + offering['d_credits']} из {max_credits}."
            else:
                try:
                    conn.execute("INSERT INTO enrollment (student_id, offering_id) VALUES (?, ?)", (student_id, offering_id))
                    conn.execute("UPDATE offering SET taken_seats = taken_seats + 1 WHERE id = ?", (offering_id,))
                    conn.commit()
                    success = True
                except sqlite3.IntegrityError:
                    error_message = "Вы уже записаны на этот поток."

    return render(request, "offerings/offering_detail.html", {
        "offering": offering,
        "error_message": error_message,
        "success": success
    })