"""Database models for the personal portfolio app.

The content is data-driven so Furqan can edit everything from the Django
admin without touching code. A singleton ``PortfolioProfile`` holds the
top-level identity and contact details, while related models store the
skills, projects, experience and services shown on the page.
"""

from django.db import models


class PortfolioProfile(models.Model):
    """Singleton model holding the core identity and contact information."""

    # --- Identity -------------------------------------------------------
    name = models.CharField(max_length=100, default="Furqan Shahid")
    short_logo = models.CharField(
        max_length=10,
        default="FS",
        help_text="Short logo/monogram shown in the navbar.",
    )
    headline = models.CharField(
        max_length=200,
        default="Python & Django Developer | Flutter Developer | Data Science Student",
    )
    identity = models.CharField(
        max_length=200,
        default=(
            "BS Data Science Student | Python & Django Developer | "
            "Flutter Developer | AI & Automation Enthusiast"
        ),
    )
    location = models.CharField(max_length=120, default="Lahore, Pakistan")

    # --- Hero -----------------------------------------------------------
    hero_text = models.TextField(
        default=(
            "I build modern web applications, mobile apps, AI-powered "
            "solutions, and automation systems while continuously exploring "
            "Data Science and Machine Learning."
        )
    )

    # --- About ----------------------------------------------------------
    about_text = models.TextField(
        default=(
            "Furqan Shahid is a BS Data Science student with a strong interest "
            "in software development, artificial intelligence, automation, and "
            "modern application development. He works with Python, Django, "
            "JavaScript, Flutter, SQL, and modern development tools. His goal "
            "is to combine software development and data-driven technologies "
            "to build useful real-world products."
        )
    )

    # --- Education ------------------------------------------------------
    degree = models.CharField(max_length=150, default="BS Data Science")
    university = models.CharField(
        max_length=150, default="University of the Punjab"
    )
    education_status = models.CharField(
        max_length=100, default="Currently studying"
    )

    # --- Contact --------------------------------------------------------
    email = models.EmailField(default="furqanshahid089@gmail.com")
    linkedin_url = models.URLField(
        blank=True, default="https://www.linkedin.com/in/furqan-shahid9878"
    )
    github_url = models.URLField(blank=True, default="https://github.com/furqanshahid089")
    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        default="+923089369211",
        help_text="Include country code, e.g. '+923089369211'. Used for the wa.me link.",
    )

    # --- Files ----------------------------------------------------------
    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        null=True,
        help_text="Uploadable resume/CV. Replaceable at any time.",
    )

    available_text = models.CharField(
        max_length=150,
        default="Available for freelance & collaboration",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio Profile"
        verbose_name_plural = "Portfolio Profile"

    def __str__(self):
        return self.name

    @property
    def whatsapp_link(self):
        """Return a wa.me link built from the digits of the number."""
        digits = "".join(ch for ch in self.whatsapp_number if ch.isdigit())
        return f"https://wa.me/{digits}" if digits else ""


class SkillCategory(models.Model):
    """A group of skills, e.g. 'Programming', 'Web Development'."""

    name = models.CharField(max_length=80)
    icon = models.CharField(
        max_length=60,
        blank=True,
        default="fa-solid fa-layer-group",
        help_text="Font Awesome class, e.g. 'fa-solid fa-code'.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Skill categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    """A single skill/badge belonging to a category."""

    category = models.ForeignKey(
        SkillCategory, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=80)
    icon = models.CharField(
        max_length=60,
        blank=True,
        help_text="Optional Font Awesome class for the badge.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Project(models.Model):
    """A portfolio project card."""

    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("ongoing", "Ongoing"),
        ("concept", "Concept / Prototype"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    technologies = models.CharField(
        max_length=250,
        help_text="Comma-separated list, e.g. 'Python, Django, SQLite'.",
    )
    features = models.TextField(
        blank=True,
        help_text="Optional. One feature per line.",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="completed"
    )
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    icon = models.CharField(
        max_length=60,
        blank=True,
        default="fa-solid fa-diagram-project",
        help_text="Font Awesome class used when no image is set.",
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        """Return technologies as a clean list for template iteration."""
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    @property
    def feature_list(self):
        """Return features as a clean list for template iteration."""
        return [f.strip() for f in self.features.splitlines() if f.strip()]


class Experience(models.Model):
    """A verified experience / volunteer entry."""

    role = models.CharField(max_length=120)
    organization = models.CharField(max_length=150)
    period = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional, e.g. 'Summer Internship Program (completed)'.",
    )
    description = models.TextField(
        blank=True, help_text="Optional summary shown above the bullet list."
    )
    responsibilities = models.TextField(
        blank=True, help_text="One responsibility per line."
    )
    icon = models.CharField(
        max_length=60, blank=True, default="fa-solid fa-hands-helping"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.role} — {self.organization}"

    @property
    def responsibility_list(self):
        return [r.strip() for r in self.responsibilities.splitlines() if r.strip()]


class Service(models.Model):
    """A 'What I Can Build' service card."""

    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(
        max_length=60, blank=True, default="fa-solid fa-code"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class TimelineItem(models.Model):
    """A step in the personal journey timeline."""

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=250, blank=True)
    icon = models.CharField(
        max_length=60, blank=True, default="fa-solid fa-circle-dot"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """A message submitted through the contact form."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"
