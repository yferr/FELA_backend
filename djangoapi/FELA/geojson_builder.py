"""
geojson_builder.py  —  Builds the complete GeoJSON response

Changes from previous version:
- agency.nombre  → agency.name
- event.country_e / event.city_e  → event.country / event.city
- speaker.country_s → speaker.country
- speaker.agency_s (string) → speaker.agency.name (FK)
- related_name 'presentations' → 'presentations_event'
- related_name 'agencies' → 'agency' (M2M field name)
- select_related / prefetch_related updated accordingly
"""
from datetime import datetime
from django.db.models import Prefetch
from .models import (
    Event, Presentation, Speaker, Agency,
    City, Country, PresentationSpeaker, EventAgency
)


class GeoJSONBuilder:
    """Builds the complete GeoJSON with the required nested structure."""

    def build_complete_geojson(self):
        return {
            "metadata": self._build_metadata(),
            "events": self._build_events(),
            "citiesGeoJSON": self._build_cities_geojson(),
            "countriesGeoJSON": self._build_countries_geojson()
        }

    def _build_metadata(self):
        total_events = Event.objects.count()
        years = Event.objects.values_list('year', flat=True).distinct().order_by('year')
        return {
            "generated_at": datetime.now().isoformat(),
            "total_events": total_events,
            "years": [year for year in years if year is not None],
            "cached": True
        }

    def _build_events(self):
        events = Event.objects.select_related('country').prefetch_related(
            Prefetch(
                'presentations_event',
                queryset=Presentation.objects.prefetch_related(
                    Prefetch(
                        'speakers',
                        queryset=Speaker.objects.select_related('country', 'agency')
                    )
                )
            ),
            Prefetch('agency', queryset=Agency.objects.all())
        ).all()

        events_structure = {}

        for event in events:
            year_key = str(event.year) if event.year else "Unknown"
            if year_key not in events_structure:
                events_structure[year_key] = {}
            if event.event_title not in events_structure[year_key]:
                events_structure[year_key][event.event_title] = []
            events_structure[year_key][event.event_title].append(
                self._build_event_data(event)
            )

        return events_structure

    def _build_event_data(self, event):
        # Agency names from M2M (field name is 'agency')
        agencies = [ag.name for ag in event.agency.all()]

        place = [{
            "country": event.country.country,   # country FK → .country string
            "city": event.city                   # city is a CharField
        }]

        titles = {}
        for presentation in event.presentations_event.all():
            titles[presentation.title] = [self._build_presentation_data(presentation)]

        return {
            "id": event.id,
            "created_by": event.created_by.username if event.created_by else None,
            "date": event.date or "",
            "type": event.type or "",
            "agency": agencies,
            "place": place,
            "titles": titles
        }

    def _build_presentation_data(self, presentation):
        speakers = []
        for speaker in presentation.speakers.all():
            country_name = speaker.country.country if speaker.country else "-"
            agency_name = speaker.agency.name if speaker.agency else ""
            speakers.append({
                "id": speaker.id,
                "created_by": speaker.created_by.username if speaker.created_by else None,
                "speaker": speaker.name,
                "country": country_name,
                "agency": agency_name
            })

        language = presentation.language if presentation.language else []

        return {
            "id": presentation.id,
            "created_by": presentation.created_by.username if presentation.created_by else None,
            "speakers": speakers,
            "language": language,
            "URL_document": presentation.url_document or "",
            "observations": presentation.observations or ""
        }

    def _build_cities_geojson(self):
        cities = City.objects.select_related('country').all()
        features = []
        for city in cities:
            if city.lon is not None and city.lat is not None:
                features.append({
                    "type": "Feature",
                    "properties": {
                        "country": city.country.country,
                        "city": city.city
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(city.lon), float(city.lat)]
                    }
                })
        return {"type": "FeatureCollection", "features": features}

    def _build_countries_geojson(self):
        countries = Country.objects.all()
        features = []
        for country in countries:
            if country.lon is not None and country.lat is not None:
                features.append({
                    "type": "Feature",
                    "properties": {"country": country.country},
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(country.lon), float(country.lat)]
                    }
                })
        return {"type": "FeatureCollection", "features": features}