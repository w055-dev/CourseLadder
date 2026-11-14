from django.shortcuts import render
from django.db.models import Sum, Count, Avg, F
from catalog.models import Discipline, Student
from offerings.models import Offering
from enrollments.models import Enrollment


def index(request):
    # Используется aggregate для получения сводки за один запрос
    stats = Offering.objects.aggregate(
        total_seats=Sum("total_seats"),
        taken_seats=Sum("taken_seats")
    )
    total_seats = stats["total_seats"] or 0
    taken_seats = stats["taken_seats"] or 0

    context = {
        "disciplines_count": Discipline.objects.count(),
        "offerings_count": Offering.objects.count(),
        "enrollments_count": Enrollment.objects.count(),
        "total_seats": total_seats,
        "taken_seats": taken_seats,
        "free_seats": total_seats - taken_seats,
    }
    return render(request, "homepage/index.html", context)


def stats(request):
    # Расчет общих сумм (без средних значений)
    general_stats = Offering.objects.aggregate(
        total_seats=Sum("total_seats"),
        taken_seats=Sum("taken_seats"),
    )

    # Расчет среднего количества свободных мест:
    free_seats_avg = Offering.objects.annotate(
        free=F("total_seats") - F("taken_seats")
    ).aggregate(avg=Avg("free"))["avg"] or 0  # сначала аннотируем, а уже затем берем среднее.

    general_stats["students_count"] = Student.objects.count()
    general_stats["disciplines_count"] = Discipline.objects.count()

    # Аннотирование: нагрузка студентов по кредитам
    student_loads = Student.objects.annotate(
        total_credits_db=Sum("enrollments__offering__discipline__credits")
    ).order_by("-total_credits_db")

    # Топ-3 популярных потока
    top_offerings = Offering.objects.annotate(
        enroll_count=Count("enrollments")
    ).filter(enroll_count__gt=0).values(
        "discipline__name", "teacher", "enroll_count"
    ).order_by("-enroll_count")[:3]

    context = {
        "stats": general_stats,
        "avg_free_seats": round(free_seats_avg, 1),  # Округляние для красоты
        "student_loads": student_loads,
        "top_offerings": top_offerings,
    }
    return render(request, "homepage/stats.html", context)
