# Inkstone Blog

Inkstone is a production-style Django blogging platform with PostgreSQL, authoring tools, profiles, comments, search, responsive UI, and persisted light/dark themes.

## Features

- Published/draft workflow, unique SEO slugs, categories, image uploads, pagination, related posts, sitemap and robots endpoint.
- Registration, login/logout, password reset/change, profile editing, and a personal dashboard.
- Ownership-enforced post/comment CRUD plus useful Django admin configuration.
- PostgreSQL-only configuration through environment variables; no credentials are stored in source.

## Requirements and PostgreSQL setup

Install Python 3.12+ and PostgreSQL. Create a database and a database user, then grant that user ownership/privileges for the database. Copy `.env.example` to `.env` and set all values:

```powershell
Copy-Item .env.example .env
```

Required variables are `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`.

## Install and run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Optional local sample content:

```bash
python manage.py seed_blog
```

Run validation:

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check
```

## Key URLs

`/` home, `/explore/`, `/categories/`, `/search/?q=django`, `/create-post/`, `/dashboard/`, `/accounts/register/`, and `/admin/`.

## Structure

`config/` holds environment-aware settings and root URLs. `blog/` owns publishing, search, comments, admin, sitemap, and the seed command. `accounts/` owns profiles and authentication views. Shared templates and assets are in `templates/` and `static/`.

## Screenshots

Add project screenshots here after running the development server.

## Future improvements

Email delivery via a transactional provider, rich-text sanitization, asynchronous image processing, and editorial review roles.
