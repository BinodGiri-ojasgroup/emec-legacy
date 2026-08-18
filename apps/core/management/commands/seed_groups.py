"""
Seeds Django Groups that mirror apps.accounts.User.Role, with sensible
default model permissions for whatever apps already have models. Safe to
re-run — it's idempotent (get_or_create throughout) and additive: it never
revokes permissions a superuser has hand-granted in Django Admin.

As later phases add real models to apps.services, apps.projects, etc., add
their permissions here rather than hand-configuring Groups in the admin UI,
so the mapping from "role" to "what they can touch" stays in version control.
"""
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db.models import Q


GROUP_APP_ACCESS = {
    "Site Administrators": {
        "apps": ["core", "pages", "accounts", "team"],
        "actions": ["add", "change", "delete", "view"],
    },
    "Content Editors": {
        "apps": ["pages", "team"],
        "actions": ["add", "change", "view"],  # no delete — singleton pages shouldn't disappear
    },
    "Research Managers": {
        "apps": ["research"],
        "actions": ["add", "change", "delete", "view"],
    },
    "Training Coordinators": {
        "apps": ["training"],
        "actions": ["add", "change", "delete", "view"],
    },
    "Careers / HR Managers": {
        "apps": ["careers"],
        "actions": ["add", "change", "delete", "view"],
    },
    "Viewers": {
        "apps": ["core", "pages", "services", "industries", "projects", "research",
                 "training", "careers", "testimonials", "blog", "media_library", "contact"],
        "actions": ["view"],
    },
}


class Command(BaseCommand):
    help = "Seed the standard EMEC permission groups (idempotent)."

    def handle(self, *args, **options):
        for group_name, config in GROUP_APP_ACCESS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            label = "Created" if created else "Updated"

            perms = Permission.objects.filter(
                content_type__app_label__in=config["apps"]
            ).filter(
                Q(*[Q(codename__startswith=action) for action in config["actions"]], _connector=Q.OR)
            )
            group.permissions.set(perms)

            self.stdout.write(self.style.SUCCESS(
                f"{label} group '{group_name}' — {perms.count()} permissions across {len(config['apps'])} app(s)."
            ))

        self.stdout.write(self.style.SUCCESS(
            "\nDone. Apps without models yet (industries, projects, testimonials, blog, "
            "media_library, contact, services beyond Viewers) will pick up real permissions "
            "automatically once their models land — just re-run this command after each phase."
        ))
