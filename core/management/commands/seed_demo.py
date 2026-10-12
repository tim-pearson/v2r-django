"""Idempotent demo data: SiteText keys, reviews and contact messages."""

from django.core.management.base import BaseCommand

from core.models import ContactMessage, Review, SiteText

# TODO: all copy below is placeholder/dummy. Client to confirm real wording.
LONG_TEXTS = {
    "hero.title": (
        "We provide project management, engineering, and support services "
        "to the infrastructure sector."
    ),
    "about.body": (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. V2R offers virtual "
        "project management and engineering support to construction and infrastructure "
        "clients. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris."
    ),
    "who.intro": (
        "Lorem ipsum dolor sit amet. V2R supports owners, developers, contractors and "
        "consultancies working across ports, marine works, pipelines, infrastructure "
        "and building projects, wherever they are in the world."
    ),
    "careers.body": (
        "Lorem ipsum dolor sit amet. We are a virtual team and welcome motivated "
        "engineers, planners and project control professionals to work with us from "
        "anywhere, on challenging infrastructure projects."
    ),
    "page.terms.body": (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Terms and conditions "
        "placeholder text. Sed do eiusmod tempor incididunt ut labore et dolore magna."
    ),
    "page.privacy.body": (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Privacy policy "
        "placeholder text. Sed do eiusmod tempor incididunt ut labore et dolore magna."
    ),
}

# TODO: client to confirm real contact details and links.
SHORT_TEXTS = {
    "header.tagline": "provide remote virtual team support work from anywhere",
    "footer.work_hours": "Monday to Friday: 9 am - 5pm\nSaturday & Sunday: Closed",
    "contact.address": (
        "FDRK 1330 Compass Building Al Shohada Road Al Hamra Industrial - FZ Ras Al Khaimah, UAE"
    ),
    "contact.phone": "+055 3472406",
    "contact.email": "contact@V2RPS.com",
    "contact.linkedin_url": "https://www.linkedin.com/company/v2r",
    "contact.whatsapp_url": "https://wa.me/0553472406",
}

SHORT_LABELS = {
    "header.tagline": "Header tagline",
    "footer.work_hours": "Footer work hours",
    "contact.address": "Contact address",
    "contact.phone": "Contact phone",
    "contact.email": "Contact email",
    "contact.linkedin_url": "Contact LinkedIn URL",
    "contact.whatsapp_url": "Contact WhatsApp URL",
}

REVIEWS = [
    (
        "Ahmed Al Mansoori",
        "Customer",
        True,
        "Excellent support on our marine project controls. Highly recommended.",
    ),
    (
        "Sarah Thompson",
        "Project Director",
        True,
        "The team delivered our tender reviews on time and with great clarity.",
    ),
    (
        "Mohammed Rashid",
        "Customer",
        True,
        "Professional, responsive and a real partner to our engineering team.",
    ),
    ("James Carter", "Customer", False, "Good early communication, awaiting final deliverables."),
    (
        "Fatima Noor",
        "Planning Manager",
        False,
        "Solid planning support so far; will update after project close-out.",
    ),
    (
        "David Okafor",
        "Customer",
        False,
        "Engaged for value engineering review - still in progress.",
    ),
]

MESSAGES = [
    (
        "Rania Haddad",
        "rania@example.com",
        "Hello, we would like to discuss support for a port project in Kuwait.",
    ),
    (
        "Peter Larsen",
        "peter@example.com",
        "Could you share details about your project planning services?",
    ),
]


class Command(BaseCommand):
    help = "Create idempotent demo content so every admin feature is visible."

    def handle(self, *args, **options):
        for key, label in {
            "hero.title": "Hero title",
            "about.body": "About body",
            "who.intro": "Who we serve intro",
            "careers.body": "Careers body",
            "page.terms.body": "Terms page body",
            "page.privacy.body": "Privacy page body",
        }.items():
            SiteText.objects.update_or_create(
                key=key, defaults={"label": label, "text": LONG_TEXTS[key]}
            )
        for key, text in SHORT_TEXTS.items():
            SiteText.objects.update_or_create(
                key=key, defaults={"text": text, "label": SHORT_LABELS.get(key, "")}
            )

        for name, role, published, text in REVIEWS:
            Review.objects.update_or_create(
                name=name,
                defaults={"role": role, "text": text, "is_published": published},
            )

        for name, email, message in MESSAGES:
            ContactMessage.objects.update_or_create(
                name=name, email=email, defaults={"message": message}
            )

        self.stdout.write(
            self.style.SUCCESS(  # pyright: ignore[reportAttributeAccessIssue]
                f"Seeded {SiteText.objects.count()} SiteTexts, "
                f"{Review.objects.count()} reviews, "
                f"{ContactMessage.objects.count()} contact messages."
            )
        )
        self.stdout.write(
            self.style.WARNING(  # pyright: ignore[reportAttributeAccessIssue]
                "Create an admin user with:  DJANGO_SUPERUSER_PASSWORD=... python manage.py "
                "createsuperuser --username admin --email you@example.com"
            )
        )
