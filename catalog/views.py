from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import Http404
from homepage.services import get_service


def discipline_list(request: HttpRequest) -> HttpResponse:
    """Список всех дисциплин."""
    service = get_service()
    return render(request, "catalog/discipline_list.html", {"disciplines": service.disciplines})


def discipline_detail(request: HttpRequest, discipline_id: int) -> HttpResponse:
    """Страница дисциплины с её потоками."""
    service = get_service()
    discipline = service.find_discipline_by_id(discipline_id)

    if discipline is None:
        raise Http404("Дисциплина не найдена")

    offerings = []
    for offering in service.offerings:
        if offering.discipline_id == discipline_id:
            offerings.append(offering)

    context = {
        "discipline": discipline,
        "offerings": offerings,
    }
    return render(request, "catalog/discipline_detail.html", context)
