from django.shortcuts import render, get_object_or_404
from django.db.models import F, Q
from django.core.paginator import Paginator
from django.db import IntegrityError
from offerings.models import Offering
from catalog.models import Student
from enrollments.models import Enrollment


def offering_list(request):
    # Аннотируем QuerySet, добавляя виртуальное поле free_seats
    offerings = Offering.objects.select_related("discipline").annotate(
        calculated_seats=F("total_seats") - F("taken_seats")
    )

    query = request.GET.get("q", "").strip()
    if query:
        offerings = offerings.filter(
            Q(discipline__name__icontains=query) |
            Q(teacher__icontains=query)
        )

    offerings = offerings.order_by("id")

    paginator = Paginator(offerings, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "query": query
    }
    return render(request, "offerings/offering_list.html", context)


def offering_detail(request, offering_id):
    # select_related, чтобы сразу получить дисциплину одним JOIN-запросом
    offering = get_object_or_404(
        Offering.objects.select_related("discipline"),
        id=offering_id
    )

    context = {
        "offering": offering
    }
    return render(request, "offerings/offering_detail.html", context)


def enroll(request, offering_id):
    offering = get_object_or_404(Offering.objects.select_related("discipline"), id=offering_id)
    error_message = ""
    success = False

    student_name = request.GET.get("student", "").strip()
    if student_name:
        student, created = Student.objects.get_or_create(full_name=student_name)

        new_total = student.current_credits + offering.discipline.credits

        if new_total > student.max_credits:
            error_message = f"Превышен лимит кредитов: {new_total} из {student.max_credits}."
        elif offering.taken_seats >= offering.total_seats:
            error_message = "На этом потоке закончились свободные места."
        else:
            try:
                Enrollment.objects.create(student=student, offering=offering)
                student.current_credits += offering.discipline.credits
                student.save()

                offering.taken_seats += 1
                offering.save()
                success = True
            except IntegrityError:
                error_message = "Вы уже записаны на этот поток."

    context = {
        "offering": offering,
        "error_message": error_message,
        "success": success
    }
    return render(request, "offerings/offering_detail.html", context)
