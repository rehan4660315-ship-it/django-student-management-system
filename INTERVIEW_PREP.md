# Interview Preparation

## Beginner
- **What is Django?** A high-level Python web framework (MTV pattern) with ORM, admin, forms, auth and security built in.
- **Why Django?** Batteries included, secure defaults (CSRF, XSS escaping, SQL-injection protection), fast development, scalable.
- **Model?** A Python class mapping to a database table (`Student`). **View?** A function or class that takes a request and returns a response. **URL?** A route in `urls.py` mapped to a view by name. **Templates?** HTML with Django tags and inheritance (`base.html`).

## Intermediate
- **CRUD:** list, detail, create/update through `ModelForm`, delete via a confirmation page and POST. Successful writes redirect (Post/Redirect/Get) with a `messages` flash.
- **ORM:** Python queries translated to parameterized SQL; e.g. `Student.objects.filter(Q(name__icontains=q) | Q(email__icontains=q))`.
- **Search:** `icontains` with `Q` objects, paginated, with `q` preserved in page links.
- **Validation:** Field validators plus `clean_<field>()` methods, run in `form.is_valid()`. The DB `unique=True` acts as a safety net.
- **Statistics:** `aggregate()` with conditional `Count(filter=Q(...))`, plus `values("course").annotate(Count("id"))`, giving 3 queries on the dashboard.
- **Authentication:** Not included; the next step is `LoginRequiredMixin` or `@login_required`.
- **CSRF:** `CsrfViewMiddleware` and `{% csrf_token %}` in every POST form. Deletion is POST-only.

## Advanced
- **Scaling:** PostgreSQL, indexes (already on `course`, `registration_date`), caching dashboard stats, gunicorn workers, a CDN for static files, background jobs.
- **SQLite to PostgreSQL:** `dumpdata`, change `DATABASES`, `migrate`, `loaddata`; verify sequences.
- **Optimizing dashboard queries:** aggregate in the DB, cache results (e.g. 60 seconds), and normalize `course` into its own indexed model.
- **Role-based access:** Django groups/permissions, `PermissionRequiredMixin`, staff vs. admin roles.
- **REST API:** Django REST Framework with `ModelSerializer` and `ModelViewSet`, token/JWT auth, pagination.
- **Deployment:** gunicorn + Nginx or PaaS, env-based secrets, `collectstatic`, HTTPS, `DEBUG=False`.
- **Production security:** `check --deploy`, HSTS, secure cookies, restricted `ALLOWED_HOSTS`, dependency updates, DB backups, rate limiting on login.
