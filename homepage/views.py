from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from homepage.services import get_service


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: сводка по данным."""
    service = get_service()

    total_seats = 0
    taken_seats = 0
    for offering in service.offerings:
        total_seats += offering.total_seats
        taken_seats += offering.taken_seats

    context = {
        "disciplines_count": len(service.disciplines),
        "offerings_count": len(service.offerings),
        "enrollments_count": len(service.enrollments),
        "total_seats": total_seats,
        "taken_seats": taken_seats,
        "free_seats": total_seats - taken_seats,
    }
    return render(request, "homepage/index.html", context)
