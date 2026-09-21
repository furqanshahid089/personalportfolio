# Furqan Shahid — Personal Portfolio

A modern, responsive personal portfolio for **Furqan Shahid**, a BS Data Science
student and developer from Lahore, Pakistan. Built with Django, it showcases
skills, projects, experience, and services, and includes a working contact form
that stores messages in the database and is manageable from the Django admin.

## Overview

- Single-page, section-based layout: Home, About, Skills, Projects, Experience,
  Services, Education, Resume, Contact.
- Content is data-driven through the Django admin — no code edits needed to
  update projects, skills, services, or profile details.
- Environment-driven configuration so the same codebase runs in development
  (SQLite) and production (PostgreSQL) without changes.

## Features

- Premium, minimal developer aesthetic with subtle glassmorphism and gradients
- Dark / light theme with preference saved in the browser
- Sticky navbar, mobile hamburger menu, smooth scrolling, active-section highlight
- Reveal-on-scroll animations that respect `prefers-reduced-motion`
- Interactive skills (badge cards), project cards with GitHub / Live / Details,
  experience, services, education, and a resume download CTA
- Accessible AJAX contact form with client + server validation, stored to the DB
- SEO: title/description, Open Graph, Twitter cards, Person schema (JSON-LD),
  favicon, `robots.txt`, and `sitemap.xml`
- Performance: lazy-loaded images, deferred JS, `font-display: swap`, minimal JS

## Tech Stack

- **Backend:** Python, Django 4.2
- **Frontend:** HTML5, CSS3 (Grid & Flexbox), vanilla JavaScript (ES6)
- **Database:** SQLite (development), PostgreSQL-ready (production)
- **Static files:** WhiteNoise
- **Config:** python-dotenv, dj-database-url

## Project Structure

```text
personal portfolio/
├── manage.py
├── requirements.txt
├── .env.example
├── vercel.json
├── README.md
│
├── myproject/                     # Django project config
│   ├── settings.py                # Env-driven settings
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── personalpotfolio/              # Portfolio app
│   ├── models.py                  # Profile, Skills, Projects, Experience, etc.
│   ├── views.py                   # home, contact, robots.txt, sitemap.xml
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── management/commands/seed_portfolio.py   # Seed default content
│
├── templates/personalpotfolio/index.html
│
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   ├── images/og-image.svg
│   └── icons/favicon.svg
│
├── media/                         # User uploads (resume, project images)
└── screenshots/                   # Add mobile/tablet/desktop captures here
```

## Installation / Setup

Requires Python 3.8+ (developed on 3.8) and pip.

```bash
# 1. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```

## Environment Setup

```bash
# Copy the example env file and edit the values
copy .env.example .env      # Windows
cp .env.example .env        # macOS / Linux
```

Key variables (see `.env.example` for the full list):

| Variable                | Purpose                                            |
| ----------------------- | -------------------------------------------------- |
| `SECRET_KEY`            | Django secret key (generate a new one for prod)    |
| `DEBUG`                 | `True` in development, `False` in production       |
| `ALLOWED_HOSTS`         | Comma-separated hostnames                          |
| `CSRF_TRUSTED_ORIGINS`  | Comma-separated origins (with scheme) for prod     |
| `DATABASE_URL`          | Empty = SQLite; set a Postgres URL for production  |

The app runs fine with no `.env` in development (sensible defaults apply).

## Running Locally

```bash
python manage.py migrate
python manage.py seed_portfolio      # Populate default content
python manage.py createsuperuser     # For the admin panel
python manage.py runserver
```

Open http://127.0.0.1:8000/ — the admin panel is at http://127.0.0.1:8000/admin/.

Submitted contact messages appear under **Contact messages** in the admin,
searchable by name/email and filterable by date (newest first).

## Testing Steps

1. **Navigation** — click every navbar link; each scrolls to its section and the
   active indicator updates.
2. **Theme** — toggle dark/light; reload the page and confirm the choice persists.
3. **Mobile** — resize below 900px; the hamburger menu opens/closes and links work.
4. **Contact form** — submit with invalid input (empty name, bad email, short
   message) to see inline errors, then submit valid input to see the success
   message and confirm the record in the admin.
5. **Reduced motion** — enable the OS "reduce motion" setting and confirm
   animations are minimized.

## Deployment

The project is deployment-ready and configured for platforms like Vercel,
Railway, or Render.

1. Set environment variables on the host: `SECRET_KEY`, `DEBUG=False`,
   `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `DATABASE_URL` (PostgreSQL).
2. Uncomment `psycopg2-binary` and `gunicorn` in `requirements.txt`.
3. Collect static files: `python manage.py collectstatic --noinput`
   (WhiteNoise serves them with compression + caching).
4. Run migrations on the host: `python manage.py migrate`.
5. Start with a production server, e.g. `gunicorn myproject.wsgi`.

> **Note on SQLite:** on ephemeral/serverless hosts (e.g. Vercel), the filesystem
> is not persistent, so use PostgreSQL via `DATABASE_URL` for contact messages
> and admin data to survive restarts.

## GitHub Setup

```bash
git init
git add .
git commit -m "Modern portfolio for Furqan Shahid"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

`.env`, `db.sqlite3`, `media/`, `staticfiles/`, and caches are already excluded
by `.gitignore`.

## Screenshots

Add captures before publishing:

- `screenshots/desktop.png`
- `screenshots/tablet.png`
- `screenshots/mobile.png`

## Placeholders to Replace

Contact details are set to Furqan's real accounts (email, GitHub, LinkedIn,
WhatsApp) and are editable any time in the Django admin under **Portfolio
Profile**. The remaining items below are optional to replace:

- **Resume** — upload a PDF in the admin (Portfolio Profile → Resume)
- **Project links** — add GitHub / Live Demo URLs per project in the admin
- **Project images** — optional; upload per project (falls back to an icon)
- **Live demo URL** — set your deployed URL and update the README
- **Screenshots** — add the three captures listed above

## Author

**Furqan Shahid** — BS Data Science Student | Developer | AI & Automation Enthusiast
