"""Django admin configuration for the portfolio app."""

from django.contrib import admin

from .models import (
    ContactMessage,
    Experience,
    PortfolioProfile,
    Project,
    Service,
    Skill,
    SkillCategory,
    TimelineItem,
)


@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
    """Singleton profile admin — one record only."""

    fieldsets = (
        ("Identity", {"fields": ("name", "short_logo", "headline", "identity", "location")}),
        ("Hero & About", {"fields": ("hero_text", "about_text", "available_text")}),
        ("Education", {"fields": ("degree", "university", "education_status")}),
        ("Contact", {"fields": ("email", "whatsapp_number", "linkedin_url", "github_url")}),
        ("Resume", {"fields": ("resume",)}),
        ("Meta", {"fields": ("updated_at",)}),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        # Enforce the singleton: only allow adding when none exists.
        return not PortfolioProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    inlines = [SkillInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "order")
    list_editable = ("status", "order")
    list_filter = ("status",)
    search_fields = ("title", "description", "technologies")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "order")
    list_editable = ("order",)
    search_fields = ("role", "organization")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
