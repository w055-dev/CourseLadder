from django.urls import path
from offerings import views


app_name = "offerings"

urlpatterns = [
    path("", views.offering_list, name="offering_list"),
    path("<int:offering_id>/", views.offering_detail, name="offering_detail"),
    path("<int:offering_id>/enroll/", views.enroll, name="enroll"),
]
