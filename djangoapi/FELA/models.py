

#from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from djangoapi.settings import EPSG_FOR_GEOMETRIES
# Create your models here.

class Country(models.Model):
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


class City(models.Model):
    #hago que apunte al id no al nombre del país
    country = models.ForeignKey(Country, on_delete=models.RESTRICT,related_name='cities')
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

 
class Agency(models.Model):
    name = models.CharField(max_length=150, unique=True)
    long_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'events"."agency'
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name


class Event(models.Model):
    date = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    #Modifico para que apunte al id del country
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='events_country_e')
    city = models.CharField(max_length=100)
    event_title = models.TextField(unique=True)
    agency = models.ManyToManyField(Agency, through='EventAgency', related_name='events_agencies')
    class Meta:
        db_table = 'events"."event'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.event_title

    @property
    def city_object(self):
        """Retorna el objeto City completo basado en country_e y city_e"""
        try:
            return City.objects.get(country=self.country, city=self.city)
        except City.DoesNotExist:
            return None


class Presentation(models.Model):
    title = models.TextField()
    #Modifico para que apunte al id de Event
    event = models.ForeignKey(Event, on_delete=models.CASCADE,  related_name='presentations_event')
    language = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        default=list
    )
    url_document = models.TextField(null=True, blank=True, db_column='url_document')
    observations = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'events"."presentation'
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentations'

    def __str__(self):
        return self.title


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    #Mofifico para que apunte a id
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, related_name='speaker_country')
    agency = models.ForeignKey(Agency, on_delete=models.RESTRICT, related_name='speaker_agency')
   
    presentations = models.ManyToManyField(
        Presentation,
        through='PresentationSpeaker',
        related_name='speakers'
    )

    class Meta:
        db_table = 'events"."speaker'
        # Constraint único por nombre + país
        unique_together = ('name', 'country')
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'

    def __str__(self):
        return f"{self.name} ({self.country.country})"


class PresentationSpeaker(models.Model):
    #Modifico para que apunte al id
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker,on_delete=models.CASCADE)

    class Meta:
        db_table = 'events"."presentation_speaker'
        unique_together = ('presentation', 'speaker')
        verbose_name = 'Presentation Speaker'
        verbose_name_plural = 'Presentation Speakers'

    def __str__(self):
        return f"{self.speaker.name} - {self.presentation.title}"


class EventAgency(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

    class Meta:
        db_table = 'events"."event_agency'
        unique_together = ('event', 'agency')
        verbose_name = 'Event Agency'
        verbose_name_plural = 'Event Agencies'

    def __str__(self):
        return f"{self.event.event_title} - {self.agency.name}"
