"""Views for the personal portfolio app."""

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ContactMessageForm
from .models import (
    Experience,
    PortfolioProfile,
    Project,
    Service,
    SkillCategory,
    TimelineItem,
)


def _get_profile():
    """Return the singleton profile.

    Tries to load (and create) the DB-backed profile. On a database-less or
    read-only deploy, fall back to an unsaved in-memory instance so the page
    still renders with the model defaults instead of crashing.
    """
    try:
        profile = PortfolioProfile.objects.first()
        if profile is None:
            profile = PortfolioProfile.objects.create()
        return profile
    except Exception:
        return PortfolioProfile()


def _safe(queryset_fn, default=None):
    """Evaluate a queryset, returning a fallback if the DB is unavailable."""
    try:
        return list(queryset_fn())
    except Exception:
        return default if default is not None else []


def home(request):
    """Render the single-page portfolio with all data-driven sections."""
    profile = _get_profile()

    context = {
        "profile": profile,
        "skill_categories": _safe(
            lambda: SkillCategory.objects.prefetch_related("skills")
        ),
        "projects": _safe(lambda: Project.objects.all()),
        "experiences": _safe(lambda: Experience.objects.all()),
        "services": _safe(lambda: Service.objects.all()),
        "timeline": _safe(lambda: TimelineItem.objects.all()),
    }
    return render(request, "personalpotfolio/index.html", context)


@require_POST
def contact(request):
    """Handle the AJAX contact form submission and persist the message."""
    form = ContactMessageForm(request.POST)

    if not form.is_valid():
        first_error = next(iter(form.errors.values()))[0]
        return JsonResponse({"ok": False, "message": first_error}, status=400)

    form.save()
    return JsonResponse(
        {"ok": True, "message": "Thanks, your message has been sent successfully."}
    )


def robots_txt(request):
    """Serve a simple robots.txt that points to the sitemap."""
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """Serve a minimal sitemap for the single-page site."""
    home_url = request.build_absolute_uri(reverse("home"))
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{home_url}</loc><changefreq>monthly</changefreq>"
        "<priority>1.0</priority></url>\n"
        "</urlset>"
    )
    return HttpResponse(xml, content_type="application/xml")
