from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'offering', 'status', 'created_at')
    list_filter = ('status', 'offering__discipline')
    search_fields = ('student__full_name', 'offering__teacher')
    # Автоматическая подгрузка связанных данных (оптимизация)
    list_select_related = ('student', 'offering')
