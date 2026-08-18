"""
Seeds realistic starter content so the site is demoable immediately and
Phase 3 (Homepage build) has real data to work against instead of empty
querysets. Safe to re-run — uses get_or_create / update_or_create
throughout. Nothing here is fake filler copy lifted from a template; it's
written specifically for EMEC's actual positioning per the project brief.
"""
from django.core.management.base import BaseCommand

from apps.blog.models import BlogCategory, Post
from apps.core.models import NavigationItem, NavigationMenu, SiteConfiguration, SocialLink
from apps.industries.models import Industry
from apps.pages.models import AboutPage, CoreValue, GroupCompany, HomePage, HomepageStatistic, ProcessStep, TimelineEvent
from apps.projects.models import Project
from apps.research.models import ResearchCategory, ResearchItem
from apps.services.models import Service, ServiceCategory, ServiceProcessStep
from apps.team.models import Department, TeamMember
from apps.testimonials.models import Client, Testimonial


class Command(BaseCommand):
    help = "Seed EMEC starter content (site config, navigation, homepage, about page). Idempotent."

    def handle(self, *args, **options):
        self._seed_site_config()
        self._seed_navigation()
        self._seed_industries()
        self._seed_services()
        self._seed_homepage()
        self._seed_process_steps()
        self._seed_about()
        self._seed_team()
        self._seed_projects()
        self._seed_research()
        self._seed_testimonials()
        self._seed_blog()
        self._seed_socials()
        self.stdout.write(self.style.SUCCESS("\nEMEC starter content seeded."))

    def _seed_site_config(self):
        config = SiteConfiguration.load()
        config.site_name = "Electro Mnemonic Engineering Consultancy"
        config.short_name = "EMEC"
        config.tagline = "Engineering the foundation of what's next."
        config.founding_year_bs = "2070"
        config.founding_year_ad = 2013
        config.primary_email = "info@emec.com.np"
        config.primary_phone = "+977-1-0000000"
        config.footer_about_text = (
            "EMEC is a multidisciplinary engineering consultancy delivering "
            "R&D, product engineering, embedded systems, automation, and AI "
            "solutions — the engineering foundation behind an entire group "
            "of companies."
        )
        config.footer_copyright_text = "© {year} EMEC — Electro Mnemonic Engineering Consultancy. All rights reserved."
        config.group_intro_text = (
            "Every company in our group exists because EMEC built the "
            "engineering capability, research culture, and technical "
            "foundation first."
        )
        config.default_meta_description = (
            "EMEC is a multidisciplinary engineering consultancy founded in "
            "2013, delivering R&D, product engineering, automation, embedded "
            "systems and AI solutions in Nepal"
        )
        config.save()
        self.stdout.write(self.style.SUCCESS("Site configuration set."))

    def _seed_navigation(self):
        primary, _ = NavigationMenu.objects.get_or_create(slot="header_primary", defaults={"label": "Header — Primary"})
        items = [
            ("Services", "/services/"),
            ("Industries", "/industries/"),
            ("Projects", "/projects/"),
            ("Research", "/research/"),
            ("Training", "/training/"),
            ("About", "/about/"),
            ("Careers", "/careers/"),
        ]
        for order, (label, url) in enumerate(items):
            NavigationItem.objects.get_or_create(
                menu=primary, label=label, parent=None,
                defaults={"url": url, "display_order": order},
            )

        footer_1, _ = NavigationMenu.objects.get_or_create(slot="footer_col_1", defaults={"label": "Footer — Company"})
        for order, (label, url) in enumerate([("About EMEC", "/about/"), ("Careers", "/careers/"), ("Blog", "/blog/"), ("Contact", "/contact/")]):
            NavigationItem.objects.get_or_create(menu=footer_1, label=label, parent=None, defaults={"url": url, "display_order": order})

        footer_2, _ = NavigationMenu.objects.get_or_create(slot="footer_col_2", defaults={"label": "Footer — Engineering"})
        for order, (label, url) in enumerate([("Services", "/services/"), ("Research", "/research/"), ("Training", "/training/"), ("Projects", "/projects/")]):
            NavigationItem.objects.get_or_create(menu=footer_2, label=label, parent=None, defaults={"url": url, "display_order": order})

        legal, _ = NavigationMenu.objects.get_or_create(slot="footer_legal", defaults={"label": "Footer — Legal"})
        for order, (label, url) in enumerate([("Privacy Policy", "/privacy/"), ("Terms of Service", "/terms/")]):
            NavigationItem.objects.get_or_create(menu=legal, label=label, parent=None, defaults={"url": url, "display_order": order})

        NavigationMenu.objects.get_or_create(slot="header_utility", defaults={"label": "Header — Utility"})
        NavigationMenu.objects.get_or_create(slot="footer_col_3", defaults={"label": "Footer — Column 3"})

        self.stdout.write(self.style.SUCCESS("Navigation menus seeded."))

    def _seed_homepage(self):
        home = HomePage.load()
        home.hero_eyebrow = "Engineering since 2070 B.S."
        home.hero_headline = "Engineering the foundation of what's next."
        home.hero_subheadline = (
            "EMEC is a multidisciplinary engineering consultancy — R&D, product "
            "engineering, embedded systems, automation, and AI — built to solve "
            "problems most firms won't take on."
        )
        home.capabilities_intro = "From concept to certified product: consulting, R&D, and engineering delivery under one roof."
        home.industries_intro = "Two decades of cross-sector engineering, from smart agriculture to industrial automation."
        home.projects_intro = "Selected engineering work across product design, automation, and embedded systems."
        home.research_intro = "Original research, prototypes, and technical publications from our engineering team."
        home.process_intro = "A disciplined, repeatable engineering process — not a one-off build."
        home.training_intro = "Corporate workshops, university partnerships, and technical courses that transfer real capability."
        home.cta_heading = "Have an engineering challenge?"
        home.cta_body = "Tell us what you're building. Our engineers will tell you how to build it right."
        home.save()

        stats = [
            ("12+", "Years of Engineering"),
            ("150+", "Projects Delivered"),
            ("40+", "Engineers & Researchers"),
            ("4", "Companies Built From EMEC's Foundation"),
        ]
        for order, (value, label) in enumerate(stats):
            HomepageStatistic.objects.get_or_create(value=value, label=label, defaults={"display_order": order})

        self.stdout.write(self.style.SUCCESS("Homepage content seeded."))

    def _seed_about(self):
        about = AboutPage.load()
        about.intro_heading = "Where Our Group Began"
        about.story = (
            "Founded in 2070 B.S. (2013 A.D.), EMEC is the first registered "
            "company in our group — and the engineering foundation everything "
            "else was built on. What started as an engineering consultancy "
            "grew into a research culture, a technical bench strength, and "
            "eventually an entire group of companies, each one made possible "
            "by capability EMEC built first."
        )
        about.vision_statement = "To be the engineering foundation that makes ambitious ideas buildable."
        about.mission_statement = (
            "We deliver rigorous, multidisciplinary engineering — research, "
            "design, and delivery — for clients and ventures who need problems "
            "solved properly, not just shipped."
        )
        about.group_story = (
            "Nepal Agro Yantra, Ojas Solutions, and RC Interior — and the "
            "ventures still to come — all exist because EMEC built the "
            "engineering capability, research culture, and technical "
            "foundation first. EMEC remains the engineering core of the group."
        )
        about.save()

        values = [
            ("Engineering Rigor", "We validate before we ship. Every solution is tested against real constraints, not assumptions."),
            ("Research Culture", "We invest in original research and prototyping, not just client delivery."),
            ("Multidisciplinary by Design", "Electrical, mechanical, embedded, and software engineers work as one team, not separate vendors."),
            ("Knowledge Transfer", "Through training and workshops, we build engineering capability in the people we work with."),
            ("Long-Term Thinking", "We've been building since 2070 B.S. Our group's other companies exist because we build things that last."),
        ]
        for order, (title, desc) in enumerate(values):
            CoreValue.objects.get_or_create(title=title, defaults={"description": desc, "display_order": order})

        timeline = [
            ("2070", 2013, "EMEC Founded", "Electro Mnemonic Engineering Consultancy registered — the first company in the group.", True),
            ("2074", 2017, "R&D Practice Established", "Formalized in-house research and prototyping capability.", False),
            ("2076", 2019, "Nepal Agro Yantra Launched", "First sister company, built on EMEC's mechanical and automation engineering foundation.", True),
            ("2078", 2021, "Ojas Solutions Launched", "Second sister company, extending EMEC's embedded systems and IoT capability.", True),
            ("2080", 2023, "RC Interior Launched", "Third sister company, applying EMEC's engineering discipline to interior systems.", True),
            ("2082", 2025, "Training & Workshop Program Expanded", "Corporate and university workshop program scaled across departments.", False),
        ]
        for order, (year_bs, year_ad, title, desc, milestone) in enumerate(timeline):
            TimelineEvent.objects.get_or_create(
                year_ad=year_ad, title=title,
                defaults={"year_bs": year_bs, "description": desc, "is_milestone": milestone, "display_order": order},
            )

        companies = [
            ("Nepal Agro Yantra", "Agricultural machinery & automation", 2019),
            ("Ojas Solutions", "Embedded systems & IoT solutions", 2021),
            ("RC Interior", "Engineering-driven interior systems", 2023),
        ]
        for order, (name, tagline, year) in enumerate(companies):
            GroupCompany.objects.get_or_create(name=name, defaults={"tagline": tagline, "founded_year": year, "display_order": order})

        self.stdout.write(self.style.SUCCESS("About page content seeded."))

    def _seed_industries(self):
        industries = [
            "Agriculture & Agro-Processing",
            "Manufacturing & Industrial",
            "Energy & Power Systems",
            "Construction & Infrastructure",
            "Automotive & Transport",
            "Consumer Electronics",
            "Healthcare Technology",
            "Education & Research Institutions",
        ]
        for order, name in enumerate(industries):
            Industry.objects.get_or_create(name=name, defaults={"display_order": order, "is_active": True})
        self.stdout.write(self.style.SUCCESS("Industries seeded."))

    def _seed_services(self):
        categories = ["Consulting & Research", "Product Engineering", "Automation & Software"]
        cat_objs = {}
        for order, name in enumerate(categories):
            cat, _ = ServiceCategory.objects.get_or_create(name=name, defaults={"slug": name.lower().replace(" & ", "-").replace(" ", "-"), "display_order": order})
            cat_objs[name] = cat

        services = [
            ("Engineering Consulting", "Consulting & Research",
             "Independent, rigorous engineering assessment before you commit capital to a build.",
             "Before a project gets funded, built, or scaled, it needs an honest engineering opinion. "
             "We assess feasibility, identify the real technical risks, and give you a straight answer "
             "on whether — and how — something should be built, drawing on 12+ years of multidisciplinary "
             "delivery across electrical, mechanical, and software engineering.",
             True),
            ("Research & Development", "Consulting & Research",
             "Original research and prototyping for problems with no off-the-shelf answer.",
             "Some problems don't have a vendor solution. Our R&D practice runs original research, builds "
             "working prototypes, and validates approaches experimentally — the same discipline that let "
             "EMEC's engineering foundation grow into an entire group of companies.",
             True),
            ("Product Design & Prototyping", "Product Engineering",
             "From concept sketch to a working, testable prototype.",
             "We take a product from a napkin sketch to a functioning prototype you can put in front of "
             "users or investors — mechanical design, electronics, and firmware integrated from day one, "
             "not bolted together at the end.",
             True),
            ("Embedded Systems & Firmware", "Product Engineering",
             "Firmware and embedded hardware engineering for connected products.",
             "Low-level firmware, embedded hardware design, and the connected-device engineering that "
             "turns a product into a platform. We've built this capability into every sister company in "
             "our group, from agricultural IoT to interior automation.",
             True),
            ("Industrial Automation", "Automation & Software",
             "PLC, SCADA, and process automation for manufacturing environments.",
             "We design and retrofit automation systems for manufacturing floors — PLC programming, SCADA "
             "integration, and the process engineering to make a production line faster and more reliable "
             "without a full equipment replacement.",
             True),
            ("AI, IoT & Custom Software", "Automation & Software",
             "Machine learning, computer vision, and IoT platforms built for industrial use.",
             "Machine learning and computer vision applied to real industrial problems — predictive "
             "maintenance, quality inspection, remote monitoring — plus the custom software and IoT "
             "platforms that make the data usable, not just collected.",
             True),
        ]
        agri = Industry.objects.filter(name__icontains="Agriculture").first()
        mfg = Industry.objects.filter(name__icontains="Manufacturing").first()
        energy = Industry.objects.filter(name__icontains="Energy").first()

        for order, (title, cat_name, summary, description, featured) in enumerate(services):
            service, _ = Service.objects.get_or_create(
                title=title,
                defaults={
                    "category": cat_objs[cat_name], "summary": summary, "description": description,
                    "is_featured": featured, "is_active": True, "display_order": order,
                },
            )
            if not service.description:
                service.description = description
                service.save(update_fields=["description"])
            if not service.process_steps.exists():
                steps = [
                    (1, "Scope & Assess", "We define the problem precisely and assess technical feasibility."),
                    (2, "Design & Validate", "Concepts and prototypes are tested before full-scale commitment."),
                    (3, "Deliver & Document", "Engineering delivery with documentation built for long-term operation."),
                ]
                for number, step_title, step_desc in steps:
                    ServiceProcessStep.objects.get_or_create(
                        service=service, step_number=number,
                        defaults={"title": step_title, "description": step_desc, "display_order": number},
                    )
            if any(i for i in [agri, mfg, energy]):
                relevant = [i for i in [agri, mfg, energy] if i]
                service.related_industries.add(*relevant[:2])

        self.stdout.write(self.style.SUCCESS("Services seeded (full Phase 5 fields)."))

    def _seed_process_steps(self):
        steps = [
            (1, "Discover", "We assess the real engineering problem, not just the requested feature."),
            (2, "Design", "Concepts, simulations, and prototypes validate the approach before major spend."),
            (3, "Build", "Multidisciplinary engineers deliver hardware, firmware, and software as one team."),
            (4, "Validate & Deliver", "Testing, documentation, and handover — built to operate for years, not demo well once."),
        ]
        for number, title, desc in steps:
            ProcessStep.objects.get_or_create(step_number=number, defaults={"title": title, "description": desc, "display_order": number})
        self.stdout.write(self.style.SUCCESS("Process steps seeded."))

    def _seed_team(self):
        eng, _ = Department.objects.get_or_create(name="Engineering", defaults={"slug": "engineering"})
        research, _ = Department.objects.get_or_create(name="Research & Innovation", defaults={"slug": "research-innovation"})

        members = [
            ("Founder & Principal Engineer", eng, "Founded EMEC in 2070 B.S. and has led its engineering practice since — from first client project to the group's three sister companies.", True),
            ("Head of Research", research, "Leads EMEC's original research and prototyping practice across embedded systems and industrial automation.", True),
            ("Head of Engineering Delivery", eng, "Oversees engineering delivery across client consulting, product design, and automation projects.", True),
        ]
        for order, (role, dept, bio, leadership) in enumerate(members):
            name = f"EMEC Team Member {order + 1}"  # placeholder identity -- replace with real names in Django Admin
            TeamMember.objects.get_or_create(
                name=name,
                defaults={
                    "role_title": role, "department": dept, "bio": bio,
                    "is_leadership": leadership, "is_active": True, "display_order": order,
                },
            )
        self.stdout.write(self.style.SUCCESS("Team seeded (placeholder names — update in Django Admin)."))

    def _seed_projects(self):
        agri = Industry.objects.filter(name__icontains="Agriculture").first()
        mfg = Industry.objects.filter(name__icontains="Manufacturing").first()
        energy = Industry.objects.filter(name__icontains="Energy").first()

        projects = [
            ("Smart Irrigation Controller", agri, "An IoT-based irrigation controller cutting water use for smallholder farms.", True),
            ("Automated Packaging Line Retrofit", mfg, "PLC-driven retrofit that raised line throughput on legacy manufacturing equipment.", True),
            ("Solar Micro-Grid Monitoring Platform", energy, "Remote monitoring and fault detection for distributed solar micro-grids.", True),
        ]
        for order, (title, industry, summary, featured) in enumerate(projects):
            Project.objects.get_or_create(
                title=title,
                defaults={
                    "industry": industry, "summary": summary, "is_featured": featured,
                    "status": Project.Status.PUBLISHED, "display_order": order,
                },
            )
        self.stdout.write(self.style.SUCCESS("Projects seeded."))

    def _seed_research(self):
        cat, _ = ResearchCategory.objects.get_or_create(name="Technical Article", defaults={"slug": "technical-article"})
        items = [
            ("Low-Cost Sensor Fusion for Agricultural IoT", "Evaluating affordable sensor combinations for smallholder-scale precision agriculture.", True),
            ("Predictive Maintenance on Legacy Industrial Equipment", "A practical approach to retrofitting vibration sensing onto equipment without native telemetry.", True),
        ]
        for order, (title, abstract, featured) in enumerate(items):
            ResearchItem.objects.get_or_create(
                title=title,
                defaults={"category": cat, "abstract": abstract, "is_featured": featured, "status": ResearchItem.Status.PUBLISHED, "display_order": order},
            )
        self.stdout.write(self.style.SUCCESS("Research items seeded."))

    def _seed_testimonials(self):
        clients = [
            ("Nepal Agro Yantra", True),
            ("Ojas Solutions", True),
            ("RC Interior", True),
        ]
        client_objs = []
        for order, (name, featured) in enumerate(clients):
            c, _ = Client.objects.get_or_create(name=name, defaults={"is_featured": featured, "display_order": order})
            client_objs.append(c)

        if client_objs:
            Testimonial.objects.get_or_create(
                author_name="Operations Lead",
                client=client_objs[0],
                defaults={
                    "author_role": "Operations",
                    "quote": "EMEC's engineering discipline is the reason our sister company could launch as fast as it did — the foundation was already built.",
                    "is_featured": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Testimonials seeded."))

    def _seed_blog(self):
        cat, _ = BlogCategory.objects.get_or_create(name="Company News", defaults={"slug": "company-news"})
        posts = [
            ("EMEC Expands Industrial Automation Practice", "New capacity added to serve manufacturing clients across Nepal.", True),
            ("Q3 Embedded Systems Workshop Announced", "Registration opens for our next corporate training cohort.", False),
        ]
        for title, excerpt, featured in posts:
            from django.utils import timezone
            Post.objects.get_or_create(
                title=title,
                defaults={"category": cat, "excerpt": excerpt, "is_featured": featured, "status": Post.Status.PUBLISHED, "published_at": timezone.now()},
            )
        self.stdout.write(self.style.SUCCESS("Blog posts seeded."))

    def _seed_socials(self):
        socials = [
            ("linkedin", "https://www.linkedin.com/company/emec-nepal", 0),
            ("facebook", "https://www.facebook.com/emecnepal", 1),
            ("youtube", "https://www.youtube.com/@emecnepal", 2),
        ]
        for platform, url, order in socials:
            SocialLink.objects.get_or_create(platform=platform, defaults={"url": url, "display_order": order})
        self.stdout.write(self.style.SUCCESS("Social links seeded."))
