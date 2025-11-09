#from django.db import models
from django.contrib.gis.db import models
from djangoapi.settings import EPSG_FOR_GEOMETRIES
# Create your models here.

class Agencies(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=150)
    long_name = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'agencies'
        verbose_name_plural = 'Agencies'
    
    def __str__(self):
        return self.nombre


class Countries(models.Model):
    country = models.CharField(primary_key=True, max_length=100)
    geom = models.PointField(srid=4326, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'countries'
        verbose_name_plural = 'Countries'
    
    def __str__(self):
        return self.country


class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(
        Countries, 
        on_delete=models.RESTRICT, 
        db_column='country'
    )
    city = models.CharField(max_length=100)
    geom = models.PointField(srid=4326, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'cities'
        unique_together = (('country', 'city'),)
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return f"{self.city}, {self.country}"


class Events(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    agency = models.TextField(blank=True, null=True)  # PostgreSQL array como texto
    type = models.CharField(max_length=100, blank=True, null=True)
    country_e = models.ForeignKey(
        Countries,
        on_delete=models.RESTRICT,
        db_column='country_e',
        related_name='events_in_country'
    )
    city_e = models.CharField(max_length=100)
    event_title = models.TextField(unique=True)
    
    class Meta:
        managed = True
        db_table = 'events'
        verbose_name_plural = 'Events'
    
    def __str__(self):
        return self.event_title


class Speakers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    country_s = models.ForeignKey(
        Countries, 
        on_delete=models.RESTRICT, 
        db_column='country_s',
        related_name='speakers_from_country'
    )
    agency_s = models.CharField(max_length=150, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'speakers'
        verbose_name_plural = 'Speakers'
    
    def __str__(self):
        return self.name


class Presentations(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    event_title = models.ForeignKey(
        Events, 
        on_delete=models.CASCADE, 
        db_column='event_title', 
        to_field='event_title'
    )
    language = models.CharField(max_length=50, blank=True, null=True)
    url_document = models.TextField(blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'presentations'
        verbose_name_plural = 'Presentations'
    
    def __str__(self):
        return self.title


class PresentationSpeakers(models.Model):
    id = models.AutoField(primary_key=True)
    id_presentation = models.ForeignKey(
        Presentations, 
        on_delete=models.CASCADE, 
        db_column='id_presentation'
    )
    id_speaker = models.ForeignKey(
        Speakers, 
        on_delete=models.CASCADE, 
        db_column='id_speaker'
    )
    
    class Meta:
        managed = True
        db_table = 'presentation_speakers'
        unique_together = (('id_presentation', 'id_speaker'),)
        verbose_name_plural = 'Presentation Speakers'
    
    def __str__(self):
        return f"{self.id_presentation} - {self.id_speaker}"


class EventsAgencies(models.Model):
    id = models.AutoField(primary_key=True)
    id_event = models.ForeignKey(
        Events, 
        on_delete=models.CASCADE, 
        db_column='id_event'
    )
    id_agencia = models.ForeignKey(
        Agencies, 
        on_delete=models.CASCADE, 
        db_column='id_agencia'
    )
    
    class Meta:
        managed = True
        db_table = 'events_agencies'
        unique_together = (('id_event', 'id_agencia'),)
        verbose_name_plural = 'Events Agencies'
    
    def __str__(self):
        return f"{self.id_event} - {self.id_agencia}"
    
class Owners(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)#optional
    dni = models.CharField(max_length=100, unique=True)#mandatory and unique