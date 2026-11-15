from django.urls import path
from catalog import views


app_name = "catalog"

urlpatterns = [
    path("", views.discipline_list, name="discipline_list"),
    path("<str:slug>/", views.discipline_detail, name="discipline_detail"),
]
