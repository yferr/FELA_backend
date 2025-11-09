from datetime import datetime
from django.db.models import Prefetch
from .models import (
    Event, Presentation, Speaker, Agency,
    City, Country, PresentationSpeaker, EventAgency
)


class GeoJSONBuilder:
    """
    Constructor del GeoJSON completo con la estructura específica requerida.
    """

    def build_complete_geojson(self):
        """
        Genera el GeoJSON completo con:
        - events: estructura anidada por año y evento
        - citiesGeoJSON: GeoJSON de ciudades
        - countriesGeoJSON: GeoJSON de países
        - metadata: información sobre la generación
        """
        return {
            "metadata": self._build_metadata(),
            "events": self._build_events(),
            "citiesGeoJSON": self._build_cities_geojson(),
            "countriesGeoJSON": self._build_countries_geojson()
        }

    def _build_metadata(self):
        """Construye metadata sobre el GeoJSON"""
        total_events = Event.objects.count()
        years = Event.objects.values_list('year', flat=True).distinct().order_by('year')
        
        return {
            "generated_at": datetime.now().isoformat(),
            "total_events": total_events,
            "years": [year for year in years if year is not None],
            "cached": True
        }

    def _build_events(self):
        """
        Construye la estructura de eventos anidada:
        {
            "2017": {
                "Event Title 1": [{ event_data }],
                "Event Title 2": [{ event_data }]
            },
            "2018": { ... }
        }
        """
        # Optimizar consultas con prefetch_related
        events = Event.objects.select_related('country_e').prefetch_related(
            Prefetch(
                'presentations',
                queryset=Presentation.objects.prefetch_related(
                    Prefetch(
                        'speakers',
                        queryset=Speaker.objects.select_related('country_s')
                    )
                )
            ),
            Prefetch(
                'agencies',
                queryset=Agency.objects.all()
            )
        ).all()

        events_structure = {}

        for event in events:
            year_key = str(event.year) if event.year else "Unknown"
            
            # Inicializar año si no existe
            if year_key not in events_structure:
                events_structure[year_key] = {}
            
            # Inicializar evento (como array con 1 elemento)
            if event.event_title not in events_structure[year_key]:
                events_structure[year_key][event.event_title] = []
            
            # Construir datos del evento
            event_data = self._build_event_data(event)
            events_structure[year_key][event.event_title].append(event_data)

        return events_structure

    def _build_event_data(self, event):
        """Construye los datos de un evento individual"""
        # Obtener agencias relacionadas
        agencies = [
            agency.nombre 
            for agency in event.agencies.all()
        ]

        # Construir lugar (array con 1 elemento)
        # ✅ CORRECCIÓN: Acceder al valor .country del objeto Country
        place = [{
            "country": event.country_e.country,  # ✅ .country para obtener el string
            "city": event.city_e  # ✅ Ya es string
        }]

        # Construir presentaciones agrupadas por título
        titles = {}
        for presentation in event.presentations.all():
            # Cada título tiene un array con 1 objeto
            titles[presentation.title] = [
                self._build_presentation_data(presentation)
            ]

        return {
            "date": event.date or "",
            "type": event.type or "",
            "agency": agencies,
            "place": place,
            "titles": titles
        }

    def _build_presentation_data(self, presentation):
        """Construye los datos de una presentación"""
        # Obtener speakers relacionados
        speakers = []
        for speaker in presentation.speakers.all():
            # ✅ CORRECCIÓN: Acceder a .country del objeto Country
            country_name = speaker.country_s.country if speaker.country_s else "-"
            
            speakers.append({
                "speaker": speaker.name,
                "country_s": country_name,  # ✅ Ahora es string
                "agency_s": speaker.agency_s or ""
            })

        # Language como array (ya es array en el modelo)
        language = presentation.language if presentation.language else []

        return {
            "speakers": speakers,
            "language": language,
            "URL_document": presentation.url_document or "",
            "observations": presentation.observations or ""
        }

    def _build_cities_geojson(self):
        """
        Construye el GeoJSON de ciudades usando cities con lat/lon
        """
        cities = City.objects.select_related('country').all()

        features = []
        for city in cities:
            # Solo incluir si tiene coordenadas
            # ✅ CORRECCIÓN: Convertir Decimal a float y acceder a .country
            if city.lon is not None and city.lat is not None:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "country": city.country.country,  # ✅ .country para obtener string
                        "city": city.city
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(city.lon),  # ✅ Convertir Decimal a float
                            float(city.lat)   # ✅ Convertir Decimal a float
                        ]
                    }
                }
                features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": features
        }

    def _build_countries_geojson(self):
        """
        Construye el GeoJSON de países usando countries con lat/lon
        """
        countries = Country.objects.all()

        features = []
        for country in countries:
            # Solo incluir si tiene coordenadas
            # ✅ CORRECCIÓN: Convertir Decimal a float
            if country.lon is not None and country.lat is not None:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "country": country.country  # ✅ Ya es el campo primary key (string)
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(country.lon),  # ✅ Convertir Decimal a float
                            float(country.lat)   # ✅ Convertir Decimal a float
                        ]
                    }
                }
                features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": features
        }