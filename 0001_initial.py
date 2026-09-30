import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(
                    message="Enter a valid phone number (7-15 digits; +, spaces, dashes and brackets allowed).",
                    regex=r"^\+?[0-9][0-9\s\-()]{6,18}$")])),
                ("course", models.CharField(max_length=100)),
                ("registration_date", models.DateField(default=django.utils.timezone.localdate)),
            ],
            options={
                "ordering": ["-registration_date", "-id"],
                "indexes": [
                    models.Index(fields=["registration_date"], name="students_st_registr_idx"),
                    models.Index(fields=["course"], name="students_st_course_idx"),
                ],
            },
        ),
    ]
