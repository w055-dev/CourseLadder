from django.shortcuts import render, get_object_or_404, redirect
from enrollments.models import Enrollment
from django.views.decorators.http import require_POST


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
    # offering = enrollment.offering
    if request.method == "POST":
        if enrollment.status == 'ACTIVE':
            enrollment.status = 'CANCELLED'
            enrollment.save()
            student = enrollment.student
            # Защита от ухода в минус
            if student.current_credits >= enrollment.offering.discipline.credits:
                student.current_credits -= enrollment.offering.discipline.credits
            else:
                student.current_credits = 0
            student.save()
        return redirect('enrollments:enrollment_list')

    context = {
        "enrollment": enrollment
    }

    return render(request, "enrollments/cancel_confirm.html", context)


@require_POST
def restore_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if enrollment.status == Enrollment.Status.CANCELLED:
        # Проверяем, не превысит ли это лимит кредитов
        student = enrollment.student
        credits = enrollment.offering.discipline.credits

        if student.current_credits + credits > student.max_credits:
            pass
        else:
            # Меняем статус обратно на ACTIVE
            enrollment.status = Enrollment.Status.ACTIVE
            enrollment.save()

            # Возвращаем кредиты
            student.current_credits += credits
            student.save()

    return redirect('enrollments:enrollment_list')
