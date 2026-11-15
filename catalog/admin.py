from django.contrib import admin
from .models import Discipline, Student


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits', 'slug')  # Отображение полей
    search_fields = ('name',)  # Поиск
    list_filter = ('credits',)  # Фильтрация
    ordering = ('name',)  # Сортировка


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'max_credits')
    search_fields = ('full_name',)
