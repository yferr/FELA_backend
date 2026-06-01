"""
admin.py  —  FELA application admin

Changes from previous version:
- All ModelAdmin classes now inherit from AuditAdmin
- AuditAdmin makes created_by, created_at, updated_at read-only
- AuditAdmin.save_model() auto-assigns request.user as created_by when creating from admin
- All field names updated to new model conventions
"""
from django.contrib import admin
from FELA import models


class AuditAdmin(admin.ModelAdmin):
    """
    Base admin that:
    - Makes audit fields read-only
    - Auto-assigns the admin user as created_by on creation
    """
    readonly_fields = ('created_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.Agency)
class AgencyAdmin(AuditAdmin):
    list_display = ('id', 'name', 'long_name', 'created_by', 'created_at')
    search_fields = ('name', 'long_name')


@admin.register(models.Country)
class CountryAdmin(AuditAdmin):
    list_display = ('id', 'country', 'lat', 'lon', 'created_by', 'created_at')
    search_fields = ('country',)


@admin.register(models.City)
class CityAdmin(AuditAdmin):
    list_display = ('id', 'city', 'country', 'lat', 'lon', 'created_by', 'created_at')
    search_fields = ('city',)


@admin.register(models.Event)
class EventAdmin(AuditAdmin):
    list_display = ('id', 'date', 'year', 'type', 'country', 'city', 'event_title', 'created_by')
    search_fields = ('event_title', 'type', 'city')


@admin.register(models.Presentation)
class PresentationAdmin(AuditAdmin):
    list_display = ('id', 'title', 'event', 'url_document', 'created_by', 'created_at')
    search_fields = ('title',)


@admin.register(models.Speaker)
class SpeakerAdmin(AuditAdmin):
    list_display = ('id', 'name', 'country', 'agency', 'created_by', 'created_at')
    search_fields = ('name',)


@admin.register(models.PresentationSpeaker)
class PresentationSpeakerAdmin(AuditAdmin):
    list_display = ('id', 'presentation', 'speaker', 'created_by')


@admin.register(models.EventAgency)
class EventAgencyAdmin(AuditAdmin):
    list_display = ('id', 'event', 'agency', 'created_by')