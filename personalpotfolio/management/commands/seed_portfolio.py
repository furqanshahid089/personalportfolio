"""Seed the portfolio with realistic default content.

Run with:  python manage.py seed_portfolio

The command is idempotent — running it again updates/creates the same
records instead of duplicating them. All content here is realistic and
based only on information provided; nothing is exaggerated or invented.
"""

from django.core.management.base import BaseCommand

from personalpotfolio.models import (
    Experience,
    PortfolioProfile,
    Project,
    Service,
    Skill,
    SkillCategory,
    TimelineItem,
)


class Command(BaseCommand):
    help = "Populate the portfolio with default skills, projects, experience and services."

    def handle(self, *args, **options):
        self._seed_profile()
        self._seed_skills()
        self._seed_projects()
        self._seed_experience()
        self._seed_services()
        self._seed_timeline()
        self.stdout.write(self.style.SUCCESS("Portfolio seeded successfully."))

    # -- Profile ---------------------------------------------------------
    def _seed_profile(self):
        if not PortfolioProfile.objects.exists():
            PortfolioProfile.objects.create()
            self.stdout.write("Created default portfolio profile.")
        else:
            # Ensure contact details match the current model defaults, without
            # overwriting any other content the user may have customised.
            profile = PortfolioProfile.objects.first()
            fields = PortfolioProfile._meta.get_field
            profile.email = profile.email or fields("email").default
            if not profile.whatsapp_number:
                profile.whatsapp_number = fields("whatsapp_number").default
            profile.save(update_fields=["email", "whatsapp_number"])
            self.stdout.write("Updated existing profile contact details.")

    # -- Skills ----------------------------------------------------------
    def _seed_skills(self):
        data = {
            "Programming": (
                "fa-solid fa-code",
                [
                    ("Python", "fa-brands fa-python"),
                    ("JavaScript", "fa-brands fa-js"),
                    ("SQL", "fa-solid fa-database"),
                    ("Dart", "fa-solid fa-bolt"),
                ],
            ),
            "Web Development": (
                "fa-solid fa-laptop-code",
                [
                    ("Django", "fa-solid fa-server"),
                    ("Django REST Framework", "fa-solid fa-plug"),
                    ("HTML5", "fa-brands fa-html5"),
                    ("CSS3", "fa-brands fa-css3-alt"),
                    ("JavaScript", "fa-brands fa-js"),
                    ("Responsive Web Development", "fa-solid fa-mobile-screen-button"),
                    ("REST APIs", "fa-solid fa-network-wired"),
                ],
            ),
            "Mobile Development": (
                "fa-solid fa-mobile-screen",
                [
                    ("Flutter", "fa-solid fa-feather"),
                    ("Dart", "fa-solid fa-bolt"),
                    ("Android Development", "fa-brands fa-android"),
                ],
            ),
            "Data & AI": (
                "fa-solid fa-brain",
                [
                    ("Data Science", "fa-solid fa-chart-line"),
                    ("Machine Learning", "fa-solid fa-robot"),
                    ("AI Integration", "fa-solid fa-microchip"),
                    ("Data Analysis", "fa-solid fa-chart-column"),
                    ("AI Automation", "fa-solid fa-gears"),
                ],
            ),
            "Tools": (
                "fa-solid fa-toolbox",
                [
                    ("Git", "fa-brands fa-git-alt"),
                    ("GitHub", "fa-brands fa-github"),
                    ("VS Code", "fa-solid fa-code"),
                    ("PyCharm", "fa-solid fa-p"),
                    ("Android Studio", "fa-brands fa-android"),
                    ("Docker", "fa-brands fa-docker"),
                    ("n8n", "fa-solid fa-diagram-project"),
                ],
            ),
        }

        for cat_order, (cat_name, (cat_icon, skills)) in enumerate(data.items()):
            category, _ = SkillCategory.objects.update_or_create(
                name=cat_name, defaults={"icon": cat_icon, "order": cat_order}
            )
            for skill_order, (skill_name, skill_icon) in enumerate(skills):
                Skill.objects.update_or_create(
                    category=category,
                    name=skill_name,
                    defaults={"icon": skill_icon, "order": skill_order},
                )

    # -- Projects --------------------------------------------------------
    def _seed_projects(self):
        projects = [
            {
                "title": "Django Quiz App",
                "description": (
                    "A Django-based quiz application where users can browse "
                    "categories, attempt quizzes, submit answers, and view "
                    "their results."
                ),
                "technologies": "Python, Django, SQLite, HTML, CSS, Bootstrap",
                "features": (
                    "Quiz categories\n"
                    "Questions and multiple-choice answers\n"
                    "Score calculation\n"
                    "Results page\n"
                    "Authentication\n"
                    "Django Admin"
                ),
                "status": "completed",
                "icon": "fa-solid fa-circle-question",
                "order": 0,
            },
            {
                "title": "Personal Portfolio",
                "description": (
                    "A professional personal portfolio website designed to "
                    "showcase skills, projects, services, and development "
                    "journey."
                ),
                "technologies": "HTML, CSS, JavaScript, Django",
                "features": "",
                "status": "completed",
                "icon": "fa-solid fa-user-astronaut",
                "order": 1,
            },
            {
                "title": "Coffee House Flutter App",
                "description": "A modern coffee shop mobile application built with Flutter.",
                "technologies": "Flutter, Dart",
                "features": (
                    "Splash screen\nLogin\nSignup\nHome\nProduct menu\n"
                    "Product details\nCart\nCheckout\nOrders\nFavorites\nProfile\n"
                    "Products: Cappuccino, Latte, Espresso, Mocha, Americano, Cold Coffee"
                ),
                "status": "completed",
                "icon": "fa-solid fa-mug-hot",
                "order": 2,
            },
            {
                "title": "AI Review & Customer Experience Agent",
                "description": (
                    "An AI-powered automation concept designed to help "
                    "businesses manage customer reviews and feedback."
                ),
                "technologies": "AI, Automation, n8n, APIs",
                "features": (
                    "Customer feedback collection\n"
                    "Sentiment analysis\n"
                    "Automated responses\n"
                    "WhatsApp/SMS communication\n"
                    "Owner notifications\n"
                    "Customer experience dashboard"
                ),
                "status": "concept",
                "icon": "fa-solid fa-comments",
                "order": 3,
            },
        ]

        for data in projects:
            Project.objects.update_or_create(
                title=data["title"], defaults=data
            )

    # -- Experience ------------------------------------------------------
    def _seed_experience(self):
        Experience.objects.update_or_create(
            role="Student Volunteer",
            organization="Alkhidmat Foundation",
            defaults={
                "period": "Summer Internship Program (completed)",
                "description": (
                    "Contributed as a student volunteer, supporting community "
                    "initiatives and coordinating with the team on activities "
                    "and events."
                ),
                "responsibilities": (
                    "Volunteer management and coordination\n"
                    "Teamwork and collaboration\n"
                    "Leadership within volunteer activities\n"
                    "Community service participation\n"
                    "Communication with team members and participants\n"
                    "Event coordination and support"
                ),
                "icon": "fa-solid fa-hands-helping",
                "order": 0,
            },
        )

    # -- Services --------------------------------------------------------
    def _seed_services(self):
        services = [
            ("Web Development", "Responsive and modern websites for individuals and businesses.", "fa-solid fa-globe"),
            ("Django Development", "Backend systems, web applications, dashboards, and APIs using Django.", "fa-solid fa-server"),
            ("Flutter App Development", "Cross-platform mobile applications using Flutter.", "fa-solid fa-mobile-screen"),
            ("AI Integration", "Integrating AI capabilities into existing applications.", "fa-solid fa-microchip"),
            ("Automation", "Workflow automation using APIs, n8n, and AI-powered systems.", "fa-solid fa-gears"),
            ("API Development", "Building and integrating REST APIs.", "fa-solid fa-plug"),
            ("Bug Fixing", "Debugging and fixing frontend/backend application issues.", "fa-solid fa-bug"),
            ("Website Deployment", "Deploying web applications and configuring production environments.", "fa-solid fa-cloud-arrow-up"),
        ]
        for order, (title, desc, icon) in enumerate(services):
            Service.objects.update_or_create(
                title=title, defaults={"description": desc, "icon": icon, "order": order}
            )

    # -- Timeline --------------------------------------------------------
    def _seed_timeline(self):
        items = [
            ("Started Learning Programming", "Began the journey into software and problem solving.", "fa-solid fa-seedling"),
            ("Python Development", "Focused on Python as a core language.", "fa-brands fa-python"),
            ("Web Development with Django", "Built web applications and backends with Django.", "fa-solid fa-server"),
            ("Mobile Development with Flutter", "Explored cross-platform apps with Flutter and Dart.", "fa-solid fa-mobile-screen"),
            ("Data Science Studies", "Pursuing BS Data Science and data-driven skills.", "fa-solid fa-chart-line"),
            ("Exploring AI / ML", "Learning machine learning and AI integration.", "fa-solid fa-brain"),
            ("Automation & AI Agents", "Building automation workflows and AI-powered systems.", "fa-solid fa-gears"),
        ]
        for order, (title, desc, icon) in enumerate(items):
            TimelineItem.objects.update_or_create(
                title=title, defaults={"description": desc, "icon": icon, "order": order}
            )
