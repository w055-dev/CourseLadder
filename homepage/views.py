from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from db.database import get_connection


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: краткая сводка по данным."""
    with get_connection() as conn:
        # Получаем общую статистику для главной страницы
        data = conn.execute("""
            SELECT 
                (SELECT COUNT(*) FROM discipline) AS disciplines_count,
                (SELECT COUNT(*) FROM offering) AS offerings_count,
                (SELECT COUNT(*) FROM enrollment) AS enrollments_count,
                (SELECT SUM(total_seats) FROM offering) AS total_seats,
                (SELECT SUM(taken_seats) FROM offering) AS taken_seats
        """).fetchone()

    total_seats = data["total_seats"] or 0
    taken_seats = data["taken_seats"] or 0
    
    context = {
        "disciplines_count": data["disciplines_count"],
        "offerings_count": data["offerings_count"],
        "enrollments_count": data["enrollments_count"],
        "total_seats": total_seats,
        "taken_seats": taken_seats,
        "free_seats": total_seats - taken_seats,
    }
    return render(request, "homepage/index.html", context)


def stats(request: HttpRequest) -> HttpResponse:
    """Страница расширенной статистики."""
    with get_connection() as conn:
        # Общая статистика
        stats_data = conn.execute("""
            SELECT 
                (SELECT COUNT(*) FROM student) AS students_count,
                (SELECT COUNT(*) FROM discipline) AS disciplines_count,
                (SELECT SUM(total_seats) FROM offering) AS total_seats,
                (SELECT SUM(taken_seats) FROM offering) AS taken_seats
        """).fetchone()
        
        # Нагрузка студентов (GROUP BY + агрегация)
        student_loads = conn.execute("""
            SELECT s.full_name, COALESCE(SUM(d.credits), 0) AS current_credits, s.max_credits
            FROM student s
            LEFT JOIN enrollment e ON s.id = e.student_id
            LEFT JOIN offering o ON e.offering_id = o.id
            LEFT JOIN discipline d ON o.discipline_id = d.id
            GROUP BY s.id
            ORDER BY current_credits DESC
        """).fetchall()

    return render(request, "homepage/stats.html", {"stats": stats_data, "student_loads": student_loads})