"""
AuditModel — Abstract base model for all FELA models.

Adds ownership and timestamp fields:
- created_by : FK to the user who created the record (auto-assigned by the ViewSet)
- created_at : timestamp of creation (auto)
- updated_at : timestamp of last update (auto)

Usage:
    class MyModel(AuditModel):
        ...
"""
from django.conf import settings
from django.db import models


class AuditModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        editable=False,
        verbose_name="Created by"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True