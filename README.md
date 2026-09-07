# JobTrack — Job Application Tracker

A full-stack **Job Application Tracker** built with **Django + Django REST Framework** (backend/API) and **server-rendered HTML + Bootstrap 5 + vanilla JavaScript + Chart.js** (frontend). Built as a portfolio project for a fresher Software Developer role — register, log in, track job applications end-to-end, schedule interviews, and visualize your progress on a dashboard.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Virtual Environment Setup](#virtual-environment-setup)
7. [MySQL Database Setup](#mysql-database-setup)
8. [Environment Variables](#environment-variables)
9. [Migrations](#migrations)
10. [Create a Superuser](#create-a-superuser)
11. [Run the Server](#run-the-server)
12. [Load Sample Data](#load-sample-data)
13. [How Authentication Works](#how-authentication-works)
14. [API Documentation](#api-documentation)
15. [Testing](#testing)
16. [Admin Panel](#admin-panel)
17. [GitHub Setup](#github-setup)
18. [Module-by-Module Explanation](#module-by-module-explanation)
19. [Screenshots](#screenshots)
20. [Future Improvements](#future-improvements)
21. [Author](#author)

---

## Project Overview

JobTrack lets a job seeker:

- Register and log in securely (JWT-based authentication)
- Add, view, edit and delete job applications
- Search, filter (status / job type / priority / date), sort and paginate applications
- Schedule and manage interview rounds per application
- View a dashboard with statistics cards, a status doughnut chart, an "applications over time" line chart, upcoming interviews, and recent applications
- Manage their profile and change their password

All data is strictly scoped to the logged-in user — no user can ever see another user's applications or interviews.

## Features

- ✅ JWT authentication (register / login / logout / token refresh)
- ✅ Full CRUD for job applications and interviews
- ✅ Company records are created/reused automatically from the application form
- ✅ Search + multi-filter (status, job type, priority, date range) + ordering + pagination
- ✅ Dashboard with Chart.js doughnut + line charts
- ✅ Responsive Bootstrap 5 UI (desktop + mobile)
- ✅ Status badges with distinct colors (Applied/Shortlisted/Interview/Selected/Rejected/Withdrawn)
- ✅ Server-side + client-side validation with readable error messages
- ✅ Centralized, safe error handling (no leaked stack traces)
- ✅ Django Admin for managing all data
- ✅ Sample/demo data management command
- ✅ Automated tests (DRF `APITestCase`) covering auth, CRUD, data isolation, filtering and dashboard stats

## Technology Stack

**Backend:** Python 3.12+, Django 5, Django REST Framework, djangorestframework-simplejwt (JWT), django-filter, MySQL

**Frontend:** HTML5, CSS3, vanilla JavaScript, Bootstrap 5, Bootstrap Icons, Chart.js

**Tools:** Git, GitHub, Postman

## Project Structure

```
jobtrack/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── jobtrack/                 # Project settings, URLs, WSGI/ASGI, custom exception handler
│   ├── settings.py
│   ├── urls.py
│   ├── exceptions.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                 # Custom User model + JWT auth (register/login/logout/profile)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── companies/                 # Company model (auto created/reused from application form)
│   ├── models.py
│   ├── serializers.py
│   └── admin.py
│
├── applications/              # JobApplication model, API, filters, sample-data command
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/load_sample_data.py
│
├── interviews/                 # Interview model + API
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── dashboard/                  # Aggregated statistics endpoint
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── tests.py
│
├── frontend/                    # Server-rendered page views (dashboard, applications, etc.)
│   ├── views.py
│   └── urls.py
│
├── templates/                   # Bootstrap 5 templates
│   ├── base.html, login.html, register.html, dashboard.html
│   ├── applications.html, application_form.html, application_detail.html
│   ├── interviews.html, interview_form.html
│   └── profile.html
│
└── static/
    ├── css/style.css
    └── js/app.js                # Shared JWT/session + fetch helpers used by every page
```

## Installation

```bash
git clone https://github.com/<your-username>/jobtrack.git
cd jobtrack
```

## Virtual Environment Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## MySQL Database Setup

1. Install MySQL Server if you don't already have it.
2. Create a database and user:

```sql
CREATE DATABASE jobtrack_db CHARACTER SET utf8mb4;
CREATE USER 'jobtrack_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON jobtrack_db.* TO 'jobtrack_user'@'localhost';
FLUSH PRIVILEGES;
```

3. That's it — this project uses **PyMySQL**, a pure-Python MySQL driver, so no C compiler or MySQL development headers are needed to install it (unlike the more common `mysqlclient` package). It works the same way on Windows, macOS, Linux, and on cloud platforms like Render.

> **Just want to try it quickly without MySQL?** Set `DB_ENGINE=sqlite` in your `.env` file and the project will use a local `db.sqlite3` file instead — no MySQL setup required. Switch back to `DB_ENGINE=mysql` for the "real" configuration described by the project spec.

## Environment Variables

Copy the example file and fill in real values:

```bash
cp .env.example .env      # macOS/Linux
copy .env.example .env    # Windows
```

`.env.example`:

```
SECRET_KEY=change-this-to-a-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=mysql
DATABASE_NAME=jobtrack_db
DATABASE_USER=root
DATABASE_PASSWORD=your_mysql_password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306

JWT_ACCESS_LIFETIME_MIN=60
JWT_REFRESH_LIFETIME_DAYS=7

CORS_ALLOW_ALL_ORIGINS=True
```

Never commit your real `.env` file — it's already excluded in `.gitignore`.

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create a Superuser

```bash
python manage.py createsuperuser
```
You'll be asked for an email, full name, and password (the custom User model uses email as the login field).

## Run the Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** — you'll be redirected to the login page if you aren't logged in yet. Register a new account, or use the sample data below.

## Load Sample Data

To explore the app immediately with realistic demo data (companies like TCS, Infosys, Wipro, Accenture, Microsoft, Amazon, Google, Deloitte, plus sample applications and interviews):

```bash
python manage.py load_sample_data
```

This creates (or reuses) a demo account:

```
Email:    demo@jobtrack.dev
Password: DemoPass123
```

Run with `--reset` to wipe and regenerate the demo user's data:

```bash
python manage.py load_sample_data --reset
```

All demo records include the note *"Sample/demo application generated by load_sample_data."* so they're clearly identifiable.

## How Authentication Works

- The API issues a **JWT access token** (short-lived) and a **refresh token** (longer-lived) on register/login.
- The frontend pages are plain Django templates; the browser stores the tokens in `localStorage` and every API call from `static/js/app.js` attaches `Authorization: Bearer <access_token>`.
- If a request gets a `401`, the app automatically tries `/api/token/refresh/` once before giving up and redirecting to `/login/`.
- Every protected page calls `JobTrack.requireAuth()` on load, which redirects to `/login/` if no token is present.
- All API endpoints (except register/login/token-refresh) require authentication, and every application/interview queryset is filtered by the logged-in user — see [API Security](#api-security-details) below.

## API Documentation

Base URL: `http://127.0.0.1:8000/api/`

### Authentication

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/api/register/` | Create a new account | No |
| POST | `/api/login/` | Log in, receive JWT tokens | No |
| POST | `/api/logout/` | Log out (validates refresh token) | Yes |
| POST | `/api/token/refresh/` | Exchange a refresh token for a new access token | No |
| GET / PUT | `/api/profile/` | View / update your profile | Yes |
| POST | `/api/profile/change-password/` | Change your password | Yes |

**POST /api/register/**
```json
// Request
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "password": "StrongPass123",
  "confirm_password": "StrongPass123"
}
// 201 Created
{
  "detail": "Account created successfully.",
  "user": {"id": 1, "full_name": "Jane Doe", "email": "jane@example.com", "created_at": "2026-01-01T10:00:00Z"},
  "tokens": {"access": "<jwt>", "refresh": "<jwt>"}
}
```

**POST /api/login/**
```json
// Request
{ "email": "jane@example.com", "password": "StrongPass123" }
// 200 OK
{
  "detail": "Login successful.",
  "user": {"id": 1, "full_name": "Jane Doe", "email": "jane@example.com", "created_at": "2026-01-01T10:00:00Z"},
  "tokens": {"access": "<jwt>", "refresh": "<jwt>"}
}
```

### Applications

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/applications/` | List (paginated), supports search/filter/ordering |
| POST | `/api/applications/` | Create |
| GET | `/api/applications/<id>/` | Retrieve one |
| PUT / PATCH | `/api/applications/<id>/` | Update |
| DELETE | `/api/applications/<id>/` | Delete |

**Query parameters:**
```
GET /api/applications/?search=python
GET /api/applications/?status=Interview
GET /api/applications/?job_type=Internship
GET /api/applications/?priority=High
GET /api/applications/?date_from=2026-01-01&date_to=2026-02-01
GET /api/applications/?ordering=-application_date
```
(All filters can be combined.)

**POST /api/applications/**
```json
// Request
{
  "company_name": "Google",
  "company_website": "https://careers.google.com",
  "job_title": "Software Engineer Intern",
  "job_type": "Internship",
  "location": "Bengaluru",
  "salary": 600000,
  "job_url": "https://careers.google.com/jobs/123",
  "application_date": "2026-01-15",
  "status": "Applied",
  "priority": "High",
  "notes": "Referred by a friend."
}
// 201 Created -> full application object, including nested "company" and "interviews": []
```

### Interviews

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/interviews/` | List (paginated) |
| POST | `/api/interviews/` | Create (requires `application` id you own) |
| GET | `/api/interviews/<id>/` | Retrieve one |
| PUT / PATCH | `/api/interviews/<id>/` | Update |
| DELETE | `/api/interviews/<id>/` | Delete |

**POST /api/interviews/**
```json
// Request
{
  "application": 1,
  "interview_date": "2026-02-01",
  "interview_time": "10:00:00",
  "interview_type": "Technical",
  "interviewer": "Alex Smith",
  "meeting_link": "https://meet.google.com/xyz",
  "result": "Pending",
  "notes": "Round 1 - DSA"
}
```

### Dashboard

**GET /api/dashboard/**
```json
{
  "total_applications": 18,
  "applied": 5, "shortlisted": 3, "interview": 4, "selected": 2, "rejected": 3, "withdrawn": 1,
  "status_breakdown": [{"status": "Applied", "count": 5}, "..."],
  "applications_over_time": [{"month": "Jan 2026", "count": 6}, "..."],
  "upcoming_interviews": [{"id": 1, "company_name": "Google", "job_title": "SWE Intern", "interview_date": "2026-09-10", "interview_time": "11:00:00", "interview_type": "Video", "meeting_link": "https://..."}],
  "recent_applications": [{"id": 18, "company_name": "Amazon", "job_title": "Backend Developer", "status": "Applied", "application_date": "2026-01-20"}]
}
```

### HTTP Status Codes Used

`200 OK` · `201 Created` · `204 No Content` (delete) · `400 Bad Request` (validation) · `401 Unauthorized` (missing/invalid token) · `403 Forbidden` · `404 Not Found` (missing or not yours) · `500 Internal Server Error` (unexpected — logged server-side, generic message returned to the client)

### API Security Details

- JWT auth (`djangorestframework-simplejwt`) on every endpoint except register/login/token-refresh.
- Every application/interview `QuerySet` is filtered by `request.user` **before** DRF even looks up the object, so a mismatched id returns `404 Not Found` (not `403`) — this avoids leaking whether the record exists.
- Object-level permission classes (`IsOwner`, `IsInterviewOwner`) provide a second layer of defense.
- `InterviewSerializer.validate_application()` rejects attaching an interview to an application you don't own.
- Passwords are hashed with Django's PBKDF2 hasher (via `set_password()`) — never stored in plain text.
- A single custom DRF exception handler (`jobtrack/exceptions.py`) ensures unexpected errors return a generic message instead of a stack trace, while still logging the real exception server-side.

### Postman

See [`postman/JobTrack.postman_collection.json`](postman/JobTrack.postman_collection.json) for a ready-to-import collection covering every endpoint above, or the plain-text walkthrough in [`postman/API_TESTING_GUIDE.md`](postman/API_TESTING_GUIDE.md).

## Testing

Run the full automated test suite:

```bash
python manage.py test
```

Covers: registration (incl. duplicate email / password mismatch / weak password), login (valid/invalid), profile view/update, password change, application CRUD, application ownership isolation, search & filtering, interview CRUD, interview ownership validation, and dashboard statistics (including per-user scoping).

## Admin Panel

```bash
python manage.py createsuperuser
python manage.py runserver
```

Visit **http://127.0.0.1:8000/admin/** to manage Users, Companies, Job Applications and Interviews, with search, filters, and ordering configured for each model.

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit: JobTrack job application tracker"
git branch -M main
git remote add origin https://github.com/<your-username>/jobtrack.git
git push -u origin main
```

Remember: `.env` is git-ignored — only `.env.example` should ever be committed.

## Deploying to Render

Render doesn't offer a managed MySQL database on its free tier, so you'll pair a **Render Web Service** (running Django) with a **free external MySQL database** (e.g. Aiven, or Railway's MySQL plugin, or PlanetScale). SQLite is *not* recommended for production on Render — its free instances use an ephemeral filesystem, so a SQLite file gets wiped on every redeploy.

1. **Push your code to GitHub** (see [GitHub Setup](#github-setup) above). `build.sh`, `render.yaml`, `gunicorn` and `whitenoise` are already included/configured in this project.

2. **Create a free MySQL database** with a provider such as [Aiven](https://aiven.io/mysql) (free trial) or Railway's MySQL add-on. Note down the host, port, database name, username and password.

3. **Create a new Web Service on Render:**
   - Go to [render.com](https://render.com) → **New +** → **Web Service** → connect your GitHub repo.
   - Render will detect `render.yaml` automatically (or configure manually):
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn jobtrack.wsgi:application`
     - **Runtime:** Python 3

4. **Set environment variables** in the Render dashboard (Environment tab):
   ```
   SECRET_KEY=<generate a long random string>
   DEBUG=False
   DB_ENGINE=mysql
   DATABASE_NAME=<your MySQL db name>
   DATABASE_USER=<your MySQL user>
   DATABASE_PASSWORD=<your MySQL password>
   DATABASE_HOST=<your MySQL host>
   DATABASE_PORT=<your MySQL port, usually 3306>
   CORS_ALLOW_ALL_ORIGINS=True
   ```
   You do **not** need to manually set `ALLOWED_HOSTS` — the project automatically trusts Render's `RENDER_EXTERNAL_HOSTNAME`, which Render sets for you.

5. **Deploy.** Render runs `build.sh` (installs dependencies, runs `collectstatic`, runs `migrate`) and then starts Gunicorn. Watch the deploy logs for errors.

6. **Create a superuser and (optionally) load sample data** using Render's **Shell** tab (under your service):
   ```bash
   python manage.py createsuperuser
   python manage.py load_sample_data
   ```

7. Visit your Render URL (e.g. `https://jobtrack.onrender.com`) — you should land on the login page.

**Troubleshooting:**
- *Static files (Bootstrap/CSS) look broken:* confirm `collectstatic` ran successfully in the build logs, and that `whitenoise` is installed (it's in `requirements.txt`).
- *"DisallowedHost" error:* double check `RENDER_EXTERNAL_HOSTNAME` is being picked up — it's set automatically by Render, so this usually means the service needs a redeploy after the first successful build.
- *Database connection errors:* verify your external MySQL provider allows external/public connections and that the host/port/credentials are exactly right.
- Free Render web services "spin down" after inactivity — the first request after idling can take 30–60 seconds to wake back up.

## Module-by-Module Explanation

- **`jobtrack/`** — Django settings (reads all secrets from `.env` via `python-decouple`), root URL configuration, and a custom DRF exception handler that keeps error responses clean and consistent.
- **`accounts/`** — A custom `User` model (`AbstractBaseUser` + `PermissionsMixin`) using **email** as the login field instead of a username. Handles registration, login (issuing JWTs), logout, profile view/update, and password change.
- **`companies/`** — A simple, shared `Company` table. The "Add Application" form only asks for a company name; `JobApplicationSerializer` transparently creates the `Company` row if it doesn't exist yet (case-insensitive match) or reuses it.
- **`applications/`** — The core `JobApplication` model plus its DRF `ModelViewSet`. `filters.py` defines a `django-filter` `FilterSet` for status/job type/priority/date-range filtering, combined with DRF's `SearchFilter` (company/job title/location) and `OrderingFilter`. `get_queryset()` always filters by `request.user`, so cross-user access is structurally impossible. Also contains the `load_sample_data` management command.
- **`interviews/`** — The `Interview` model (foreign key to `JobApplication`), scoped the same way through the related application's owner. `InterviewSerializer.validate_application()` double-checks ownership on write.
- **`dashboard/`** — A single aggregation endpoint that computes status counts, a monthly trend (via `TruncMonth`), upcoming interviews, and the 5 most recent applications — all scoped to the logged-in user.
- **`frontend/`** — Thin `TemplateView`s that just render the HTML shell for each page. All real data loading happens client-side via `fetch()` calls to the API (see `static/js/app.js`), keeping the authentication and business logic in one place (the API) while still using plain Django templates as required by the stack.
- **`templates/` & `static/`** — Bootstrap 5 markup, a shared `app.js` with the JWT/session helpers (`apiFetch`, `requireAuth`, `statusBadge`, flash messages, etc.), and `style.css` for the JobTrack visual theme, including the six status badge colors.

## Screenshots

*(Add screenshots of the Dashboard, Applications list, Application detail, and Add Application form here before publishing your portfolio.)*

```
screenshots/
├── dashboard.png
├── applications-list.png
├── application-detail.png
└── add-application-form.png
```

## Future Improvements

- Email notifications/reminders for upcoming interviews
- Resume/document attachments per application
- Kanban-style drag-and-drop board view (by status)
- Export applications to CSV/PDF
- Multi-language support
- Refresh-token blacklisting on logout (requires `token_blacklist` app + Redis/DB storage)
- Rate limiting on auth endpoints

## Author

Built as a fresher Software Developer portfolio / interview-demonstration project.

**JobTrack** — track every application, one row at a time.
