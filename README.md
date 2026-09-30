# EduManage: Django Student Management System

A responsive student administration dashboard built with Django, Bootstrap 5 and Chart.js.

## Features
- Dashboard with live statistics (total, unique courses, this month, last 7 days), Students-by-Course chart, course table and recent students
- Student CRUD with a delete confirmation page (deletion only via POST)
- Search by name or email (partial, case-insensitive) with pagination
- Server-side validation: name, unique email (case-insensitive), phone, course, no future dates
- Initials avatars, course badges, success/error alerts, empty states, responsive sidebar
- Django admin configured; tests included

## Tech Stack
Python, Django 5, Django ORM, HTML/CSS/JS, Bootstrap 5 + Bootstrap Icons (CDN), Chart.js (CDN), SQLite (dev), PostgreSQL (prod)

## Project Structure
```text
student_management/
├── manage.py
├── requirements.txt
├── .env.example
├── student_management/   (settings, urls, wsgi)
└── students/
    ├── models.py  forms.py  views.py  urls.py  admin.py  tests.py
    ├── migrations/0001_initial.py
    ├── templatetags/student_extras.py
    └── templates/students/  (base, dashboard, student_list, student_detail, student_form, student_confirm_delete)
```

## Installation
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```
Open http://127.0.0.1:8000/

## Existing database?
If you already have a `students_student` table from your old project, back it up first. Duplicate emails must be removed before `unique=True` can apply. Then use your own migrations (`makemigrations` / `migrate`) or delete `db.sqlite3` for a fresh start.

## Testing
```bash
python manage.py test
```

## Environment variables
See `.env.example`: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, and `DB_*` for PostgreSQL.

## Deployment (summary)
1. `pip install "psycopg[binary]" gunicorn whitenoise`, and set `DB_ENGINE=postgres` plus the `DB_*` variables.
2. Set `DJANGO_DEBUG=False`, a strong `DJANGO_SECRET_KEY`, and `DJANGO_ALLOWED_HOSTS`.
3. Add WhiteNoise middleware (admin static files), then run `python manage.py collectstatic` and `python manage.py migrate`.
4. Serve with `gunicorn student_management.wsgi` behind HTTPS (Nginx or a platform such as Render/Railway).
5. Moving data from SQLite: `dumpdata --natural-foreign > data.json`, switch DB, `migrate`, `loaddata data.json`.
6. Check with `python manage.py check --deploy`.

## Screenshots
Add your screenshots to a `screenshots/` folder and link them here.

## Future Improvements
Authentication and roles, CSV export, a Course model, registration trend chart, REST API (DRF), file/photo upload.
