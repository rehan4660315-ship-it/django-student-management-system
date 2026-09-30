from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

phone_validator = RegexValidator(
    regex=r"^\+?[0-9][0-9\s\-()]{6,18}$",
    message="Enter a valid phone number (7-15 digits; +, spaces, dashes and brackets allowed).",
)


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[phone_validator])
    course = models.CharField(max_length=100)
    registration_date = models.DateField(default=timezone.localdate)

    class Meta:
        ordering = ["-registration_date", "-id"]
        indexes = [
            models.Index(fields=["registration_date"], name="students_st_registr_idx"),
            models.Index(fields=["course"], name="students_st_course_idx"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("student_detail", args=[self.pk])
