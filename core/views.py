from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm, ReviewForm
from .models import ContactMessage, Review, SiteText

# Hardcoded card content (not in the DB). TODO: client to confirm wording.
SERVICES = [
    {
        "title": "Project Management Systems",
        "subheading": "Project Management Systems",
        "items": [
            "PM System Development",
            "Project Controls Systems",
            "System Maturity Models",
            "Project Procedures",
            "Consultation/Advisory",
        ],
    },
    {
        "title": "Front End Project Development",
        "subheading": "Project Structuring & Scope Definition",
        "items": [
            "Project Brief",
            "Concept Designs",
            "FEED Support",
            "Tender Document Review",
            "Tender Process Support",
            "Alternative Design & Solutions",
        ],
    },
    {
        "title": "Project Planning & Analysis",
        "subheading": "Detailed Planning",
        "items": [
            "Programs & Planning",
            "Resource Scheduling",
            "Value Engineering",
            "Option Analysis",
            "Risk Assessments",
            "Alternative Solutions",
            "Execution Strategies",
        ],
    },
    {
        "title": "Project Deliverables",
        "subheading": "Execution Phase Level of Detail",
        "items": [
            "Execution Strategy",
            "Detailed Design",
            "Methods of Work",
            "Sequences of Work",
            "Temporary Works",
        ],
    },
    {
        "title": "Review Services",
        "subheading": "Conduct Reviews & Report",
        "items": [
            "Tender Documents",
            "Technical Reviews",
            "Contract Reviews",
            "Bid / Tender Reviews",
            "Design Reviews",
            "Constructability",
            "Overflow Work",
        ],
    },
    {
        "title": "Other Support Services",
        "subheading": "Detailed Planning",
        "items": [
            "Visualization (2D/3D)",
            "Engineering Support",
            "Independent Assessment",
            "Claim Prevention Strategies",
            "3D+ Visualization Claim Support",
        ],
    },
]

EXPERIENCE = [
    {
        "title": "Key Project Types",
        "items": [
            "Port & Harbor Works",
            "Jetties & Wharves",
            "Pipelines - Land & Marine",
            "Tender Document Review",
            "Breakwaters - Coastal Protection",
            "Temporary Works",
        ],
    },
    {
        "title": "Project Phases",
        "items": [
            "Project Development",
            "Front End Studies",
            "Budgets & Estimates",
            "Tendering & Proposals",
            "Design & Engineering",
            "Pre-Construction",
            "Project Start Ups",
            "Project monitoring & controls",
            "Package Management",
        ],
    },
    {
        "title": "Process Experience",
        "items": [
            "Scope Management",
            "Requirements Management",
            "Time - planning",
            "Resource Management",
            "Cost Management",
            "Engineering Management",
            "Production Management",
            "Project Controls",
            "Risk Management",
            "Change Management",
            "Issue Management",
            "Value Engineering",
            "Process Maturity Studies",
            "Peer Review Process",
            "Quality Management",
            "HSE Management",
            "Claims Management",
        ],
    },
    {
        "title": "Activity Based - Civil",  # TODO: client to confirm title
        "items": [
            "Site Conditions - Survey",
            "Geotechnical Investigation",
            "Steel Piling Works",
            "Concrete Piling - bored cast insitu",
            "Sheet Piled Structures",
            "Combi-Wall Structures",
            "Precast Concrete Works",
            "Temporary Works",
            "Earthworks",
            "Ground Improvement",
            "Reinforced Concrete Works",
            "Marine Cofferdams",
            "Land Based Cofferdams",
        ],
    },
    {
        "title": "Activity Based - Marine/Pipelines",  # TODO: client to confirm title
        "items": [
            "Bridge Works",
            "Breakwaters & Revetments",
            "Marina Works",
            "Marine Pipeline Works",
            "Land Based Pipelines",
            "HDPE Pipeline",
            "GRP Pipeline",
            "Carbon steel Pipeline",
            "Building Works",
        ],
    },
]

# Images live in static/img/work/. The user adds real ones; the view falls back
# to a placeholder tile when a file is missing. TODO: real projects.
WORK = [
    {"title": "Port Expansion Project", "image": "img/work/port_expansion_project.jpg"},
    {"title": "Jetties & Wharves", "image": "img/work/jetties_and_wharves.jpg"},
    {"title": "Marine Pipelines", "image": "img/work/marine_pipelines.jpg"},
    {"title": "Land Reclamation", "image": "img/work/land_reclamation.jpg"},
    {"title": "Breakwater Works", "image": "img/work/breakwater_works.jpg"},
]

# TODO: client to confirm the client types.
WHO = [
    "Owners & Developers",
    "Main Contractors",
    "Engineering Consultants",
    "Government & Infrastructure Authorities",
]

STATIC_DIR = Path(settings.BASE_DIR) / "static"


def _with_image_ok(items):
    out = []
    for item in items:
        out.append({**item, "ok": (STATIC_DIR / item["image"]).exists()})
    return out


def _home_context(contact_form=None):
    work = _with_image_ok(WORK)
    return {
        "services": SERVICES,
        "experience": EXPERIENCE,
        "who": WHO,
        "work_tiles": work[1:],
        "featured": work[0],
        "reviews": Review.objects.filter(is_published=True),
        "contact_form": contact_form or ContactForm(),
    }


def home(request):
    return render(request, "home.html", _home_context())


def review_form(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                name=form.cleaned_data["name"],
                role=form.cleaned_data["role"] or "Customer",
                text=form.cleaned_data["text"],
                is_published=False,
            )
            messages.success(
                request, "Thank you! Your review has been submitted and is awaiting moderation."
            )
            return redirect(reverse("review_thanks"))
    else:
        form = ReviewForm()
    return render(request, "review_form.html", {"form": form})


def review_thanks(request):
    return render(request, "review_thanks.html")


def contact_submit(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect(f"{reverse('home')}#contact")
        messages.error(request, "Please correct the errors below.")
        return render(request, "home.html", _home_context(form), status=400)
    return redirect(f"{reverse('home')}#contact")


def generic_page(request, slug):
    key = f"page.{slug}.body"
    if not SiteText.objects.filter(key=key).exists():
        raise Http404(f"No page content for '{slug}'")
    return render(
        request,
        "generic_page.html",
        {"slug": slug, "page_title": slug.replace("-", " ").title(), "page_key": key},
    )
