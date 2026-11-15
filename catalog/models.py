from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Discipline(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, blank=True)
    credits = models.PositiveIntegerField(verbose_name="Кредиты")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)  # Автогенерация slug из названия
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:discipline_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=200, unique=True, verbose_name="ФИО")
    max_credits = models.PositiveIntegerField(default=30, verbose_name="Лимит кредитов")
    current_credits = models.PositiveIntegerField(default=0, verbose_name="Текущие кредиты")

    def __str__(self):
        return self.full_name
