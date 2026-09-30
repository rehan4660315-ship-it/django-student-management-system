from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "course", "registration_date")
    list_filter = ("course", "registration_date")
    search_fields = ("name", "email", "phone")
    date_hierarchy = "registration_date"
