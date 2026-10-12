# V2R — Virtual to Reality

Small, mostly static marketing site for V2R, a virtual project management and
engineering support company for the construction/infrastructure sector.

- Django 5.2 LTS, SQLite, one app (`core`), three models.
- The client edits site text in the Django admin; nothing else needs touching.
- Plain CSS (`static/css/style.css`) + one vanilla JS file (`static/js/main.js`).

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo        # idempotent demo content
.venv/bin/python manage.py runserver
```

### Create an admin user (no password is stored in the repo)

```bash
DJANGO_SUPERUSER_PASSWORD='pick-a-strong-one' \
  .venv/bin/python manage.py createsuperuser \
  --username admin --email you@example.com
```

Then log in at `/admin/` and edit the SiteText rows.

## Environment variables (all optional, dev-safe defaults)

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | insecure dev key | Secret key. Set in production. |
| `DJANGO_DEBUG` | `true` | Debug mode. |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated host list. |
| `DJANGO_SHOW_TEXT_REFS` | same as DEBUG | Reference badges on/off. |

## The reference tag (`{% site_text %}`)

Long editable texts render through `core/templatetags/v2r_tags.py`:

```
{% site_text "about.body" %}
{% site_text "header.tagline" plain %}   # no badge
```

- When `SHOW_TEXT_REFS` is on (default in dev), long texts are wrapped in a
  `span.text-ref` with a small blue badge `[key]` that links straight to the
  SiteText's admin change page. The client sees the reference, clicks it, edits.
- When off, it outputs plain text only.
- `plain` never shows a badge (use it for short values: tagline, work hours,
  contact details).
- A missing key renders a visible `[text missing: key]` placeholder, never crashes.

Badge is intended only for the long texts:
`hero.title`, `about.body`, `who.intro`, `careers.body`, `page.terms.body`, `page.privacy.body`.

## Models

- **SiteText** — the only editable content: `key` (unique, `[a-z0-9._-]+`),
  `text`, optional `label` (admin helper), `updated_at`.
- **Review** — public reviews; the public form creates unpublished ones and only
  published reviews show on the site.
- **ContactMessage** — messages from the contact form. (No email sending yet, TODO.)

Service/Experience cards are hardcoded lists in `core/views.py`, not in the DB.
Images are static files under `static/img/` (the client adds real photos; missing
files fall back to placeholders).

## Static / media

- `static/` — CSS, JS, and images (collect with `python manage.py collectstatic`
  for production; Whitenoise serves them).
- `media/` — user uploads (currently unused; MEDIA_URL is served in DEBUG).

## Verify before shipping

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python manage.py test
.venv/bin/ruff check .
.venv/bin/ruff format .
```

## URLs

| Path | View |
| --- | --- |
| `/` | Home (single scrolling page) |
| `/review/` | Public review form |
| `/review/thanks/` | Review thank-you |
| `/contact/` | Contact form POST |
| `/p/<slug>/` | Generic page (needs `page.<slug>.body` SiteText), 404 otherwise |

## TODOs

- Real copy, photos, logo, contact details and social URLs (all marked in code).
- Link targets for View All / Learn More / Life At V2R / Current Positions
  (currently point at generic `/p/...` pages).
- Email sending for contact messages.