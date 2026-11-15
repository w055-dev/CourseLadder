from django.db import models
from catalog.models import Student
from offerings.models import Offering


class EnrollmentQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Enrollment.Status.ACTIVE)

    def for_student(self, student_name):
        return self.filter(student__full_name__icontains=student_name)


class EnrollmentManager(models.Manager):
    def get_queryset(self):
        return EnrollmentQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Активна'
        CANCELLED = 'CANCELLED', 'Отменена'
        COMPLETED = 'COMPLETED', 'Завершена'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = EnrollmentManager()

    def __str__(self):
        return f"{self.student.full_name} -> {self.offering.discipline.name}"

    class Meta:
        unique_together = ('student', 'offering')
