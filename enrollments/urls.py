from django.urls import path
from enrollments import views


app_name = "enrollments"

urlpatterns = [
    path("", views.enrollment_list, name="enrollment_list"),
    path("cancel/<int:enrollment_id>/", views.cancel_enrollment, name="cancel"),
    path("restore/<int:enrollment_id>/", views.restore_enrollment, name="restore")
]
