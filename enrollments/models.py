from django.db import models
from catalog.models import Student
from offerings.models import Offering


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    offering = models.ForeignKey(Offering, on_delete=models.CASCADE, related_name="enrollments")

    class Meta:
        unique_together = ('student', 'offering')
