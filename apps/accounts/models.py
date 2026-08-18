"""
EMEC — custom User model.

A custom user model is defined from the very first migration (rather than
retrofitted later) per Django best practice — swapping AUTH_USER_MODEL after
tables exist is a painful migration. It stays a thin extension of
AbstractUser: authentication itself is unchanged, we only add the fields
Django Admin needs to reason about *who* can edit *what* across a
multi-department content site (Content, Research, Training, HR/Careers).

`role` is deliberately coarse — it drives which permission Group a person
is seeded into (see apps/core/management/commands/seed_groups.py) — not a
replacement for Django's Group/Permission system. Fine-grained access still
goes through Groups so it stays editable from Django Admin without a code
change.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models_base import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    class Role(models.TextChoices):
        SITE_ADMIN = "site_admin", "Site Administrator"
        CONTENT_EDITOR = "content_editor", "Content Editor"
        RESEARCH_MANAGER = "research_manager", "Research Manager"
        TRAINING_COORDINATOR = "training_coordinator", "Training Coordinator"
        CAREERS_MANAGER = "careers_manager", "Careers / HR Manager"
        VIEWER = "viewer", "Viewer (read-only)"

    role = models.CharField(
        max_length=30, choices=Role.choices, default=Role.VIEWER,
        help_text="Determines which permission group this account is seeded into.",
    )
    job_title = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="staff/avatars/", blank=True, null=True)
    is_department_head = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name() or self.username
