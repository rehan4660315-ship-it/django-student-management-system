from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import StudentForm
from .models import Student

PAGE_SIZE = 10


def dashboard(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    week_ago = today - timedelta(days=7)

    stats = Student.objects.aggregate(
        total=Count("id"),
        courses=Count("course", distinct=True),
        this_month=Count("id", filter=Q(registration_date__gte=month_start)),
        last_7_days=Count("id", filter=Q(registration_date__gte=week_ago)),
    )
    course_stats = list(
        Student.objects.values("course").annotate(total=Count("id")).order_by("-total", "course")
    )
    recent_students = Student.objects.order_by("-registration_date", "-id")[:8]

    return render(request, "students/dashboard.html", {
        "stats": stats,
        "course_stats": course_stats,
        "chart_data": {
            "labels": [c["course"] for c in course_stats],
            "values": [c["total"] for c in course_stats],
        },
        "recent_students": recent_students,
    })


def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(Q(name__icontains=query) | Q(email__icontains=query))
    students = students.order_by("name", "id")

    paginator = Paginator(students, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "students/student_list.html", {
        "page_obj": page_obj,
        "query": query,
        "total_count": paginator.count,
    })


def student_detail(request, pk):
    return render(request, "students/student_detail.html", {"student": get_object_or_404(Student, pk=pk)})


def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect("student_list")
    return render(request, "students/student_form.html", {"form": form, "is_edit": False})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student information updated successfully.")
        return redirect("student_detail", pk=student.pk)
    return render(request, "students/student_form.html", {"form": form, "student": student, "is_edit": True})


@require_http_methods(["GET", "POST"])
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})
