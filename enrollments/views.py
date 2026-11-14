from django.shortcuts import render, get_object_or_404, redirect
from enrollments.models import Enrollment


def enrollment_list(request):
    # Получаем все записи, оптимизируем запросы
    enrollments = Enrollment.objects.select_related(
        "student", "offering__discipline"
    ).order_by("student__full_name")

    context = {
        "enrollments": enrollments
    }
    return render(request, "enrollments/enrollment_list.html", context)


def cancel_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    offering = enrollment.offering
    if request.method == "POST":
        # Удаление
        enrollment.delete()
        student = enrollment.student
        student.current_credits -= enrollment.offering.discipline.credits
        student.save()
        # Освобождение места
        offering.taken_seats -= 1
        offering.save()
        return redirect('enrollments:enrollment_list')

    context = {
        "enrollment": enrollment
    }

    return render(request, "enrollments/cancel_confirm.html", context)
