from django.shortcuts import render
from db.database import get_connection


def enrollment_list(request):
    with get_connection() as conn:
        # JOIN трех таблиц
        enrollments = conn.execute("""
        SELECT e.id AS enrollment_id, s.full_name AS student_name, 
            d.id AS discipline_id, d.name AS discipline_name, 
            o.id AS offering_id, o.teacher 
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        JOIN offering o ON e.offering_id = o.id
        JOIN discipline d ON o.discipline_id = d.id
        ORDER BY s.full_name
    """).fetchall()
    return render(request, "enrollments/enrollment_list.html", {"enrollments": enrollments})