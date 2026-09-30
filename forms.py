import re

from django import forms
from django.utils import timezone

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "phone", "course", "registration_date"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Ali Raza"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+92 300 1234567"}),
            "course": forms.TextInput(attrs={"placeholder": "e.g. Django"}),
            "registration_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        letters_only = re.sub(r"[ .'\-]", "", name)
        if not letters_only or not letters_only.isalpha():
            raise forms.ValidationError("Name may only contain letters, spaces, dots, apostrophes and hyphens.")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        duplicates = Student.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = re.sub(r"\D", "", phone)
        if not 7 <= len(digits) <= 15:
            raise forms.ValidationError("Phone number must contain 7 to 15 digits.")
        return phone

    def clean_course(self):
        course = " ".join(self.cleaned_data["course"].split())
        if not course:
            raise forms.ValidationError("Course is required.")
        return course

    def clean_registration_date(self):
        date = self.cleaned_data["registration_date"]
        if date > timezone.localdate():
            raise forms.ValidationError("Registration date cannot be in the future.")
        return date
