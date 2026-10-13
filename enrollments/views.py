from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from homepage.services import get_service


def enrollment_list(request: HttpRequest) -> HttpResponse:
    """Список всех записей студентов."""
    service = get_service()

    rows = []
    for enrollment in service.enrollments:
        offering = service.find_offering_by_id(enrollment.offering_id)
        discipline = None
        if offering is not None:
            discipline = service.find_discipline_by_id(
                offering.discipline_id
            )
        rows.append({
            "enrollment": enrollment,
            "offering": offering,
            "discipline": discipline,
        })

    return render(request, "enrollments/enrollment_list.html", {"rows": rows})
