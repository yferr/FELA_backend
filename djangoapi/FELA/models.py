"""
models.py  —  FELA application models

Changes from previous version:
- All models now inherit from AuditModel (adds created_by, created_at, updated_at)
- managed = True  →  Django creates and manages all tables via migrations
- Schema changed from  eventos"."<plural>  to  events"."<singular>
- Field renames (tutor conventions):
    Agency  : nombre       → name
    Event   : country_e   → country,   city_e → city
    Speaker : country_s   → country,   agency_s (CharField) → agency (ForeignKey)
    Presentation : event_title (FK to text) → event (FK to id)
    PresentationSpeaker : id_presentation → presentation, id_speaker → speaker
    EventAgency         : id_event → event, id_agencia → agency
- No manual primary keys (Django generates id automatically)
"""

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from djangoapi.settings import EPSG_FOR_GEOMETRIES
from .audit import AuditModel


# ---------------------------------------------------------------------------
# Country
# ---------------------------------------------------------------------------

class Country(AuditModel):
    country = models.CharField(max_length=100, unique=True)
    geom = models.PointField(srid=4326, null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    lon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        db_table = 'events"."country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country


# ---------------------------------------------------------------------------
# City
# ---------------------------------------------------------------------------

class City(AuditModel):
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name='cities'
    )
    city = models.CharField(max_length=100)
    geom = models.PointField(srid=4326, null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    lon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        db_table = 'events"."city'
        unique_together = ('country', 'city')
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.city}, {self.country.country}"


# ---------------------------------------------------------------------------
# Agency
# ---------------------------------------------------------------------------

class Agency(AuditModel):
    name = models.CharField(max_length=150, unique=True)
    long_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'events"."agency'
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Event
# ---------------------------------------------------------------------------

class Event(AuditModel):
    date = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name='events_country_e'
    )
    city = models.CharField(max_length=100)
    event_title = models.TextField(unique=True)
    agency = models.ManyToManyField(
        Agency,
        through='EventAgency',
        related_name='events_agencies'
    )

    class Meta:
        db_table = 'events"."event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.event_title

    @property
    def city_object(self):
        """Returns the full City object based on country and city name."""
        try:
            return City.objects.get(country=self.country, city=self.city)
        except City.DoesNotExist:
            return None


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

class Presentation(AuditModel):
    title = models.TextField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='presentations_event'
    )
    language = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        default=list
    )
    url_document = models.TextField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'events"."presentation'
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentations'

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Speaker
# ---------------------------------------------------------------------------

class Speaker(AuditModel):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        related_name='speaker_country'
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.RESTRICT,
        related_name='speaker_agency',
        null=True,
        blank=True
    )
    presentations = models.ManyToManyField(
        Presentation,
        through='PresentationSpeaker',
        related_name='speakers'
    )

    class Meta:
        db_table = 'events"."speaker'
        unique_together = ('name', 'country')
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'

    def __str__(self):
        return f"{self.name} ({self.country.country})"


# ---------------------------------------------------------------------------
# PresentationSpeaker  (intermediate table)
# ---------------------------------------------------------------------------

class PresentationSpeaker(AuditModel):
    presentation = models.ForeignKey(
        Presentation,
        on_delete=models.CASCADE
    )
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'events"."presentation_speaker'
        unique_together = ('presentation', 'speaker')
        verbose_name = 'Presentation Speaker'
        verbose_name_plural = 'Presentation Speakers'

    def __str__(self):
        return f"{self.speaker.name} — {self.presentation.title}"


# ---------------------------------------------------------------------------
# EventAgency  (intermediate table)
# ---------------------------------------------------------------------------

class EventAgency(AuditModel):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'events"."event_agency'
        unique_together = ('event', 'agency')
        verbose_name = 'Event Agency'
        verbose_name_plural = 'Event Agencies'

    def __str__(self):
        return f"{self.event.event_title} — {self.agency.name}"