from django.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    credits = models.PositiveIntegerField(verbose_name="Кредиты")

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=200, unique=True, verbose_name="ФИО")
    max_credits = models.PositiveIntegerField(default=30, verbose_name="Лимит кредитов")
    current_credits = models.PositiveIntegerField(default=0, verbose_name="Текущие кредиты")

    def __str__(self):
        return self.full_name
