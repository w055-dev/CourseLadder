from django.urls import path
from enrollments import views


app_name = "enrollments"

urlpatterns = [
    path("", views.enrollment_list, name="enrollment_list"),
]
