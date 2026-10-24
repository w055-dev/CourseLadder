from django.shortcuts import render
from django.http import Http404
from db.database import get_connection


def discipline_list(request):
    with get_connection() as conn:
        disciplines = conn.execute("SELECT id, name, credits FROM discipline ORDER BY name").fetchall()
    return render(request, "catalog/discipline_list.html", {"disciplines": disciplines})


def discipline_detail(request, discipline_id):
    with get_connection() as conn:
        discipline = conn.execute(""""
                                  SELECT *, (total_seats - taken_seats) AS free_seats
                                   FROM discipline
                                    WHERE id = ?
                                """, (discipline_id,)).fetchall()
        if not discipline:
            raise Http404("Дисциплина не найдена")
        offerings = conn.execute("SELECT * FROM offering WHERE discipline_id = ?", (discipline_id,)).fetchall()
    return render(request, "catalog/discipline_detail.html", {"discipline": discipline, "offerings": offerings})
