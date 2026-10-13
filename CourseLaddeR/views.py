from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Кастомная страница 404."""
    return render(request, "404.html", status=404)
