from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import StudentForm
from .models import Student
from .templatetags.student_extras import initials


def make_student(**kw):
    n = Student.objects.count() + 1
    data = dict(name=f"Student {n}".replace(str(n), "Test"), email=f"s{n}@example.com",
                phone="+92 300 1234567", course="Django", registration_date=timezone.localdate())
    data.update(kw)
    return Student.objects.create(**data)


def form_data(**kw):
    data = {"name": "Ali Raza", "email": "ali@example.com", "phone": "+92 300 1234567",
            "course": "Django", "registration_date": timezone.localdate().isoformat()}
    data.update(kw)
    return data


class ModelTests(TestCase):
    def test_create_and_str(self):
        self.assertEqual(str(make_student(name="Ali Raza")), "Ali Raza")

    def test_email_unique(self):
        make_student(email="a@example.com")
        with self.assertRaises(IntegrityError), transaction.atomic():
            make_student(email="a@example.com")

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            Student(name="", email="", phone="", course="").full_clean()

    def test_initials_filter(self):
        self.assertEqual(initials("Ali Raza"), "AR")
        self.assertEqual(initials("Ali"), "AL")


class FormTests(TestCase):
    def test_valid(self):
        self.assertTrue(StudentForm(form_data()).is_valid())

    def test_invalid_email(self):
        self.assertIn("email", StudentForm(form_data(email="nope")).errors)

    def test_missing_fields(self):
        form = StudentForm({})
        for f in ("name", "email", "phone", "course"):
            self.assertIn(f, form.errors)

    def test_duplicate_email_case_insensitive(self):
        make_student(email="ali@example.com")
        self.assertIn("email", StudentForm(form_data(email="ALI@example.com")).errors)

    def test_edit_keeps_own_email(self):
        s = make_student(email="ali@example.com")
        self.assertTrue(StudentForm(form_data(), instance=s).is_valid())

    def test_bad_phone_and_name_and_future_date(self):
        self.assertIn("phone", StudentForm(form_data(phone="abc")).errors)
        self.assertIn("name", StudentForm(form_data(name="1234")).errors)
        future = (timezone.localdate() + timedelta(days=5)).isoformat()
        self.assertIn("registration_date", StudentForm(form_data(registration_date=future)).errors)


class ViewTests(TestCase):
    def test_list_and_detail(self):
        s = make_student(name="Ali Raza")
        self.assertContains(self.client.get(reverse("student_list")), "Ali Raza")
        self.assertContains(self.client.get(reverse("student_detail", args=[s.pk])), "Ali Raza")

    def test_detail_404(self):
        self.assertEqual(self.client.get(reverse("student_detail", args=[999])).status_code, 404)

    def test_create(self):
        r = self.client.post(reverse("student_create"), form_data(), follow=True)
        self.assertRedirects(r, reverse("student_list"))
        self.assertContains(r, "Student added successfully.")
        self.assertEqual(Student.objects.count(), 1)

    def test_create_invalid(self):
        r = self.client.post(reverse("student_create"), form_data(email="bad"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)

    def test_update(self):
        s = make_student()
        r = self.client.post(reverse("student_update", args=[s.pk]), form_data(name="New Name"), follow=True)
        self.assertContains(r, "updated successfully")
        s.refresh_from_db()
        self.assertEqual(s.name, "New Name")

    def test_delete_requires_post(self):
        s = make_student()
        self.assertContains(self.client.get(reverse("student_delete", args=[s.pk])), "cannot be undone")
        self.assertEqual(Student.objects.count(), 1)
        r = self.client.post(reverse("student_delete", args=[s.pk]), follow=True)
        self.assertContains(r, "Student deleted successfully.")
        self.assertEqual(Student.objects.count(), 0)


class SearchTests(TestCase):
    def setUp(self):
        make_student(name="Ali", email="a1@example.com")
        make_student(name="Ali Raza", email="a2@example.com")
        make_student(name="Muhammad Ali", email="a3@example.com")
        make_student(name="Sara Khan", email="sara@school.org")

    def test_by_name_partial(self):
        r = self.client.get(reverse("student_list"), {"q": "ali"})
        self.assertEqual(r.context["total_count"], 3)

    def test_by_email(self):
        r = self.client.get(reverse("student_list"), {"q": "school.org"})
        self.assertEqual(r.context["total_count"], 1)

    def test_no_results(self):
        r = self.client.get(reverse("student_list"), {"q": "zzzz"})
        self.assertContains(r, "No Results Found")


class DashboardTests(TestCase):
    def test_empty(self):
        self.assertContains(self.client.get(reverse("dashboard")), "No Students Yet")

    def test_stats(self):
        make_student(course="Python")
        make_student(course="Python")
        make_student(course="Django", registration_date=timezone.localdate() - timedelta(days=400))
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.context["stats"]["total"], 3)
        self.assertEqual(r.context["stats"]["courses"], 2)
        self.assertEqual(r.context["course_stats"][0], {"course": "Python", "total": 2})
        self.assertEqual(len(r.context["recent_students"]), 3)

    def test_recent_limited_to_eight(self):
        for _ in range(10):
            make_student()
        self.assertEqual(len(self.client.get(reverse("dashboard")).context["recent_students"]), 8)
