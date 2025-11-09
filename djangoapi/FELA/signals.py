from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import (
    Event, Presentation, Speaker, Agency,
    PresentationSpeaker, EventAgency,
    City, Country
)


GEOJSON_CACHE_KEY = 'geojson_complete'


def invalidate_geojson_cache():
    """Invalida el caché del GeoJSON"""
    cache.delete(GEOJSON_CACHE_KEY)
    print(f"[CACHE] GeoJSON cache invalidated at {GEOJSON_CACHE_KEY}")


# Signals para Event
@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def event_changed(sender, instance, **kwargs):
    """Invalida caché cuando un evento cambia"""
    invalidate_geojson_cache()


# Signals para Presentation
@receiver(post_save, sender=Presentation)
@receiver(post_delete, sender=Presentation)
def presentation_changed(sender, instance, **kwargs):
    """Invalida caché cuando una presentación cambia"""
    invalidate_geojson_cache()


# Signals para Speaker
@receiver(post_save, sender=Speaker)
@receiver(post_delete, sender=Speaker)
def speaker_changed(sender, instance, **kwargs):
    """Invalida caché cuando un speaker cambia"""
    invalidate_geojson_cache()


# Signals para Agency
@receiver(post_save, sender=Agency)
@receiver(post_delete, sender=Agency)
def agency_changed(sender, instance, **kwargs):
    """Invalida caché cuando una agencia cambia"""
    invalidate_geojson_cache()


# Signals para relaciones
@receiver(post_save, sender=PresentationSpeaker)
@receiver(post_delete, sender=PresentationSpeaker)
def presentation_speaker_changed(sender, instance, **kwargs):
    """Invalida caché cuando cambia relación presentation-speaker"""
    invalidate_geojson_cache()


@receiver(post_save, sender=EventAgency)
@receiver(post_delete, sender=EventAgency)
def event_agency_changed(sender, instance, **kwargs):
    """Invalida caché cuando cambia relación event-agency"""
    invalidate_geojson_cache()


# Signals para coordenadas
@receiver(post_save, sender=City)
@receiver(post_delete, sender=City)
def city_temp_changed(sender, instance, **kwargs):
    """Invalida caché cuando cambian coordenadas de ciudades"""
    invalidate_geojson_cache()


@receiver(post_save, sender=Country)
@receiver(post_delete, sender=Country)
def country_temp_changed(sender, instance, **kwargs):
    """Invalida caché cuando cambian coordenadas de países"""
    invalidate_geojson_cache()