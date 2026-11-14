from django.shortcuts import render, get_object_or_404
from catalog.models import Discipline


def discipline_list(request):
    # Получаем все дисциплины, сортируем по названию
    disciplines = Discipline.objects.all().order_by("name")
    context = {
        "disciplines": disciplines
    }
    return render(request, "catalog/discipline_list.html", context)


def discipline_detail(request, discipline_id):
    discipline = get_object_or_404(Discipline, id=discipline_id)  # get_object_or_404 автоматически вернет 404, если нет такого id

    # Получаем потоки этой дисциплины через обратную связь related_name="offerings"
    offerings = discipline.offerings.all().order_by("teacher")

    context = {
        "discipline": discipline,
        "offerings": offerings
    }

    return render(request, "catalog/discipline_detail.html", context)
