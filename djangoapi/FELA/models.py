

#from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField

from djangoapi.settings import EPSG_FOR_GEOMETRIES
# Create your models here.


class Country(models.Model):
    country = models.CharField(max_length=100, unique=True, primary_key=True)
    geom = models.PointField(srid=4326, null=True, blank=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    lon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'eventos"."countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country


class City(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        db_column='country',
        related_name='cities'
    )
    city = models.CharField(max_length=100)
    geom = models.PointField(srid=4326, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    lon = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'eventos"."cities'
        unique_together = ('country', 'city')
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.city}, {self.country.country}"

 
class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)
    long_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos"."agencies'
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.nombre


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    country_e = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        db_column='country_e',
        related_name='events'
    )
    city_e = models.CharField(max_length=100)
    event_title = models.TextField(unique=True)
    agencies = models.ManyToManyField(
        Agency,
        through='EventAgency',
        related_name='events'
    )

    class Meta:
        managed = False
        db_table = 'eventos"."events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.event_title

    @property
    def city_object(self):
        """Retorna el objeto City completo basado en country_e y city_e"""
        try:
            return City.objects.get(country=self.country_e, city=self.city_e)
        except City.DoesNotExist:
            return None


class Presentation(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    event_title = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        db_column='event_title',
        to_field='event_title',
        related_name='presentations'
    )
    language = ArrayField(
        models.CharField(max_length=50),
        blank=True,
        null=True,
        default=list
    )
    url_document = models.TextField(null=True, blank=True, db_column='url_document')
    observations = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'eventos"."presentations'
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentations'

    def __str__(self):
        return self.title


class Speaker(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    country_s = models.ForeignKey(
        Country,
        on_delete=models.RESTRICT,
        db_column='country_s',
        related_name='speakers'
    )
    agency_s = models.CharField(max_length=150, null=True, blank=True)
    presentations = models.ManyToManyField(
        Presentation,
        through='PresentationSpeaker',
        related_name='speakers'
    )

    class Meta:
        managed = False
        db_table = 'eventos"."speakers'
        # Constraint único por nombre + país
        unique_together = ('name', 'country_s')
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'

    def __str__(self):
        return f"{self.name} ({self.country_s.country})"


class PresentationSpeaker(models.Model):
    id_presentation = models.ForeignKey(
        Presentation,
        on_delete=models.CASCADE,
        db_column='id_presentation'
    )
    id_speaker = models.ForeignKey(
        Speaker,
        on_delete=models.CASCADE,
        db_column='id_speaker'
    )

    class Meta:
        managed = False
        db_table = 'eventos"."presentation_speakers'
        unique_together = ('id_presentation', 'id_speaker')
        verbose_name = 'Presentation Speaker'
        verbose_name_plural = 'Presentation Speakers'

    def __str__(self):
        return f"{self.id_speaker.name} - {self.id_presentation.title}"


class EventAgency(models.Model):
    id_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        db_column='id_event'
    )
    id_agencia = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        db_column='id_agencia'
    )

    class Meta:
        managed = False
        db_table = 'eventos"."events_agencies'
        unique_together = ('id_event', 'id_agencia')
        verbose_name = 'Event Agency'
        verbose_name_plural = 'Event Agencies'

    def __str__(self):
        return f"{self.id_event.event_title} - {self.id_agencia.nombre}"
