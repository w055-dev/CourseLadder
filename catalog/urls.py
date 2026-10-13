from django.urls import path
from catalog import views


app_name = "catalog"

urlpatterns = [
    path("", views.discipline_list, name="discipline_list"),
    path("<int:discipline_id>/", views.discipline_detail, name="discipline_detail"),
]
