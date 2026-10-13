from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from homepage.services import get_service
from src.services import ServiceError


def offering_list(request: HttpRequest) -> HttpResponse:
    """Список всех потоков."""
    service = get_service()

    rows = []
    for offering in service.offerings:
        discipline = service.find_discipline_by_id(
            offering.discipline_id
        )
        rows.append({
            "offering": offering,
            "discipline": discipline,
        })

    return render(request, "offerings/offering_list.html", {"rows": rows})


def offering_detail(request: HttpRequest, offering_id: int) -> HttpResponse:
    """Страница потока с подробностями."""
    service = get_service()
    offering = service.find_offering_by_id(offering_id)

    if offering is None:
        raise Http404("Поток не найден")

    discipline = service.find_discipline_by_id(offering.discipline_id)

    context = {
        "offering": offering,
        "discipline": discipline,
    }
    return render(request, "offerings/offering_detail.html", context)


def enroll(request: HttpRequest, offering_id: int) -> HttpResponse:
    service = get_service()
    offering = service.find_offering_by_id(offering_id)

    if offering is None:
        raise Http404("Поток не найден")

    student_name = request.GET.get("student", "").strip()
    if student_name == "":
        # Имя не передано => Редирект на страницу потока
        return redirect("offerings:offering_detail", offering_id=offering_id)

    from src.models import Student
    student = Student(student_name)

    for enrollment in service.enrollments:
        if enrollment.student == student.name:
            student.add_enrollment(enrollment)

    error_message = ""
    try:
        service.enroll(student, offering_id)
    except ServiceError as exc:
        error_message = str(exc)

    discipline = service.find_discipline_by_id(offering.discipline_id)

    context = {
        "offering": offering,
        "discipline": discipline,
        "error_message": error_message,
        "success": error_message == "",
    }
    return render(request, "offerings/offering_detail.html", context)
