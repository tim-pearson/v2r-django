# AGENTS.md: v2r-django

Small, mostly static marketing site for V2R ("Virtual to Reality"), a virtual project
management and engineering support company for the construction/infrastructure sector.
The backend is minimal. The client edits text in the Django admin.

## Golden rule: DO NOT OVER-ENGINEER
- Allowed: Python 3.11, Django 5.2 LTS, SQLite, Pillow, djangoql, whitenoise (optional).
- Not allowed: DRF, Celery, Postgres, Docker files, Node/npm build steps, JS frameworks,
  icon libraries, i18n, CSS frameworks.
- One Django project package `config`, ONE app `core`.
- Plain CSS in `static/css/style.css`, one small vanilla JS file `static/js/main.js`.
- No new models, packages or apps without asking me first.

## Models (only these three)
- `SiteText`: `key` (CharField, unique, regex `[a-z0-9._-]+`, e.g. `about.body`),
  `text` (TextField), `label` (optional, admin helper), `updated_at`.
  This is the ONLY model for client-editable content.
- `Review`: name, role (default "Customer"), text, `is_published` (default False),
  created_at. The public form creates UNPUBLISHED reviews. Only published ones show.
- `ContactMessage`: name, email, message, created_at.

Service/Experience cards are HARDCODED (a small list of dicts in `views.py` or the
template), not in the DB. Images are static files I add myself under `static/img/`.

## SiteText keys
`hero.title`, `about.body`, `who.intro`, `careers.body`, `page.terms.body`,
`page.privacy.body`, `header.tagline`, `footer.work_hours`, `contact.address`,
`contact.phone`, `contact.email`, `contact.linkedin_url`, `contact.whatsapp_url`.
Which ones show a reference badge is controlled by the `label` field, not by the key:
any SiteText with a non-empty `label` gets a badge when `SHOW_TEXT_REFS` is on.

## Reference tag feature
`{% site_text "about.body" %}` is in `core/templatetags/v2r_tags.py`.
- When `settings.SHOW_TEXT_REFS` is True (default = DEBUG) AND the SiteText has a
  non-empty `label`, it wraps the text in `<span class="text-ref">` plus a small
  badge showing the key, linking to the admin change page for that SiteText. The
  client sees the reference, opens the admin and edits.
- The badge opens in a new tab and uses `settings.HOSTED_URL` (env var `HOSTED_URL`,
  default `http://127.0.0.1:8000`) plus the admin path, so it resolves from any host.
- When False, or when the SiteText has no label, it outputs plain text only.
- A missing key renders a visible placeholder, never a crash.
- `{% site_text "key" plain %}` never shows a badge (use inside href attributes,
  e.g. the social URLs).

## Pages
- Home is one scrolling page with anchored sections: Home, About, Services, Who We Serve,
  Areas of Experience, Contact Us. Layout details are in `docs/design/LAYOUT.md`.
- Pages that don't exist yet (Terms, Privacy, "View All", "Learn More", "Life at V2R",
  "Current Positions") use ONE generic view at `/p/<slug>/`: a title plus the SiteText
  `page.<slug>.body`, 404 if missing. No per-page templates or models.
- `/review/` is the public review form. Contact and review forms use standard Django
  forms, CSRF, a honeypot field and `django.contrib.messages`. No email sending (TODO).

## Admin
- Every ModelAdmin uses `djangoql.admin.DjangoQLSearchMixin`.
- Titles: "V2R Admin".
- Review: `list_editable` on `is_published`, `list_filter` on `is_published`,
  actions "Publish selected" and "Unpublish selected".
- SiteText: list_display key/label/updated_at, search on key and text.
- If a ForeignKey is ever added, it must be visible and a clickable link to the related
  admin page (TODO: add a small helper then, not before).

## Seed data
`python manage.py seed_demo` is idempotent. It creates all SiteText keys with
recognisable lorem text, about 6 Reviews (3 published, 3 unpublished) and a couple of
ContactMessages, so every feature is visible in the admin.
Footer placeholder values (mark `# TODO: client to confirm`):
address "FDRK 1330 Compass Building Al Shohada Road Al Hamra Industrial - FZ Ras Al Khaimah, UAE",
phone "+055 3472406", email "contact@V2RPS.com".
Never hardcode passwords. Document `createsuperuser` with env vars in the README.

## Frontend rules
- Mobile-first CSS with ONE breakpoint at 900px (documented in a comment).
- Narrow screens: compact header (logo left, small menu button right). The button opens a
  panel sliding in from the RIGHT (about 80% width, max 320px) with a dim overlay. It
  closes on overlay click, link click or Escape, and uses `aria-expanded`/`aria-controls`.
- Wide screens: header as in the layout doc, no hamburger.
- Inline SVG for icons. No remote assets or CDNs. Everything works offline.
- Where an image is missing, use a simple placeholder and add `# TODO` or `<!-- TODO -->`.

## Verify after every change (run these, don't guess)
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python manage.py test`
- `ruff check .` and `ruff format .`
Fix failures before moving on. Keep tests to a few smoke tests: home returns 200,
a submitted review is unpublished, the site_text badge/plain toggle, `/p/<slug>/` 404.

## Workflow
- Work in checkpoints. STOP after each one and wait for my OK:
  1 scaffold and settings, 2 models and admin, 3 site_text tag,
  4 seed_demo, 5 base/header/hero/drawer, 6 services and experience,
  7 remaining sections and footer, 8 forms, 9 responsive and JS polish,
  10 README, .gitignore and tests.
- Small commits per checkpoint, if git is initialised.
- Leave `# TODO:` for anything you can't fill in (logo, photos, real links and copy).
- Keep code small and readable. No premature abstractions.
- If the spec conflicts with this file, ask me before proceeding.