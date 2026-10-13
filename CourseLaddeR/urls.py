from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("disciplines/", include("catalog.urls")),
    path("offerings/", include("offerings.urls")),
    path("enrollments/", include("enrollments.urls")),
]


# Кастомная обработка 404
handler404 = "CourseLaddeR.views.page_not_found"
