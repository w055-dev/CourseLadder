from django.db import models
from catalog.models import Discipline


class Offering(models.Model):
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="offerings"
    )
    teacher = models.CharField(max_length=150, verbose_name="Преподаватель")
    total_seats = models.PositiveIntegerField(default=30, verbose_name="Всего мест")
    taken_seats = models.PositiveIntegerField(default=0, verbose_name="Занято мест")

    def __str__(self):
        return f"{self.discipline.name} - {self.teacher}"

    @property
    def free_seats(self):
        active_taken = self.enrollments.filter(status='ACTIVE').count()
        return self.total_seats - active_taken

    @property
    def active_taken_seats(self):
        """Возвращает количество активных записей на этот поток."""
        return self.enrollments.filter(status='ACTIVE').count()
