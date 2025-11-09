from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q

from .models import (
    Country, City, Agency, Event, Presentation, 
    Speaker, PresentationSpeaker, EventAgency
)
from .serializers import (
    CountrySerializer, CountryDetailSerializer,
    CitySerializer,
    AgencySerializer,
    EventSerializer, EventDetailSerializer, EventCompleteCreateSerializer,
    PresentationSerializer, PresentationDetailSerializer,
    SpeakerSerializer, SpeakerDetailSerializer
)


# ============== VIEWSETS CON AUTOCOMPLETADO ==============

class CountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para países con búsqueda (autocomplete).
    
    GET /api/eventos/countries/?search=esp
    → Retorna países que contienen "esp" (case-insensitive)
    """
    queryset = Country.objects.all()
    permission_classes = [AllowAny]  # Cambiar a IsAuthenticated cuando configures usuarios
    lookup_field = 'country'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['country']  # Búsqueda case-insensitive por defecto
    ordering_fields = ['country']
    ordering = ['country']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CountryDetailSerializer
        return CountrySerializer
    
    def get_queryset(self):
        """
        Personalizar queryset para búsqueda más flexible.
        """
        queryset = Country.objects.all()
        
        # Búsqueda manual adicional si es necesario
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(country__icontains=search)
        
        return queryset


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ciudades con búsqueda y filtro por país.
    
    GET /api/eventos/cities/?search=val
    → Retorna ciudades que contienen "val"
    
    GET /api/eventos/cities/?country=España
    → Retorna ciudades de España
    
    GET /api/eventos/cities/?search=bar&country=España
    → Retorna ciudades de España que contienen "bar"
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['city']
    filterset_fields = ['country__country']
    ordering_fields = ['city', 'country']
    ordering = ['country__country', 'city']
    
    def get_queryset(self):
        """
        Filtrado personalizado por país (case-insensitive).
        """
        queryset = City.objects.select_related('country').all()
        
        # Filtro por país (case-insensitive)
        country_param = self.request.query_params.get('country')
        if country_param:
            queryset = queryset.filter(country__country__iexact=country_param)
        
        # Búsqueda por ciudad (case-insensitive)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(city__icontains=search)
        
        return queryset


class AgencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para agencias con búsqueda (autocomplete).
    
    GET /api/eventos/agencies/?search=unesco
    → Retorna agencias que contienen "unesco"
    """
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        queryset = Agency.objects.all()
        
        # Búsqueda manual adicional
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        
        return queryset


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet para eventos con búsqueda por título.
    Incluye acción custom para crear evento completo.
    
    GET /api/eventos/events/?search=gis
    → Retorna eventos que contienen "gis" en el título
    """
    queryset = Event.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['event_title']
    filterset_fields = ['year', 'type', 'country_e__country']
    ordering_fields = ['year', 'event_title']
    ordering = ['-year']
    
    def get_serializer_class(self):
        if self.action == 'create_complete':
            return EventCompleteCreateSerializer
        elif self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.select_related('country_e').prefetch_related(
            'presentations', 'agencies'
        ).all()
        
        # Filtros adicionales
        year = self.request.query_params.get('year')
        country = self.request.query_params.get('country')
        event_type = self.request.query_params.get('type')
        search = self.request.query_params.get('search')
        
        if year:
            queryset = queryset.filter(year=year)
        if country:
            queryset = queryset.filter(country_e__country__iexact=country)
        if event_type:
            queryset = queryset.filter(type__icontains=event_type)
        if search:
            queryset = queryset.filter(event_title__icontains=search)
        
        return queryset
    
    @action(detail=False, methods=['post'], url_path='create-complete')
    def create_complete(self, request):
        """
        Crea un evento completo con presentaciones y speakers en una sola operación.
        Normaliza automáticamente (case-insensitive get-or-create).
        
        POST /api/eventos/events/create-complete/
        
        Body ejemplo:
        {
            "date": "2025-01-15",
            "year": 2025,
            "type": "Conference",
            "country": "España",
            "city": "Valencia",
            "event_title": "GIS Summit 2025",
            "country_lat": 40.4168,
            "country_lon": -3.7038,
            "city_lat": 39.4699,
            "city_lon": -0.3763,
            "agencies": ["UNESCO", "FAO"],
            "presentations": [
                {
                    "title": "ML in GIS",
                    "language": ["en", "es"],
                    "url": "http://...",
                    "observations": "...",
                    "speakers": [
                        {
                            "name": "Juan Pérez",
                            "country": "España",
                            "agency": "CSIC"
                        }
                    ]
                }
            ]
        }
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(
                EventDetailSerializer(event).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresentationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para presentaciones con búsqueda compleja.
    
    GET /api/eventos/presentations/?search=machine
    → Retorna presentaciones con "machine" en el título
    """
    queryset = Presentation.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'event_title__year']
    ordering = ['-event_title__year']
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'search']:
            return PresentationDetailSerializer
        return PresentationSerializer
    
    def get_queryset(self):
        queryset = Presentation.objects.select_related(
            'event_title',
            'event_title__country_e'
        ).prefetch_related('speakers').all()
        return queryset
    
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Búsqueda compleja de presentaciones con múltiples filtros.
        
        Query params:
        - event_id: ID del evento
        - event_title: Título del evento (búsqueda parcial)
        - speaker_id: ID del speaker
        - speaker_name: Nombre del speaker (búsqueda parcial)
        - language: Idioma
        - agency: Nombre de agencia (búsqueda en agencias del evento)
        - country: País del evento
        - year: Año del evento
        
        Ejemplo: /api/eventos/presentations/search/?language=es&country=España&year=2025
        """
        queryset = self.get_queryset()
        
        # Filtro por evento
        event_id = request.query_params.get('event_id')
        event_title = request.query_params.get('event_title')
        if event_id:
            queryset = queryset.filter(event_title__id=event_id)
        if event_title:
            queryset = queryset.filter(event_title__event_title__icontains=event_title)
        
        # Filtro por speaker
        speaker_id = request.query_params.get('speaker_id')
        speaker_name = request.query_params.get('speaker_name')
        if speaker_id:
            queryset = queryset.filter(speakers__id=speaker_id)
        if speaker_name:
            queryset = queryset.filter(speakers__name__icontains=speaker_name)
        
        # Filtro por idioma
        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(language__contains=[language])
        
        # Filtro por país del evento
        country = request.query_params.get('country')
        if country:
            queryset = queryset.filter(event_title__country_e__country__iexact=country)
        
        # Filtro por año
        year = request.query_params.get('year')
        if year:
            queryset = queryset.filter(event_title__year=year)
        
        # Filtro por agencia (del evento)
        agency = request.query_params.get('agency')
        if agency:
            queryset = queryset.filter(
                event_title__agencies__nombre__icontains=agency
            )
        
        # Eliminar duplicados
        queryset = queryset.distinct()
        
        serializer = PresentationDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class SpeakerViewSet(viewsets.ModelViewSet):
    """
    ViewSet para speakers con búsqueda.
    
    GET /api/eventos/speakers/?search=juan
    → Retorna speakers con "juan" en el nombre
    
    GET /api/eventos/speakers/?country=España
    → Retorna speakers de España
    """
    queryset = Speaker.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'agency_s']
    filterset_fields = ['country_s__country']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpeakerDetailSerializer
        return SpeakerSerializer
    
    def get_queryset(self):
        queryset = Speaker.objects.select_related('country_s').all()
        
        # Filtro por país (case-insensitive)
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country_s__country__iexact=country)
        
        # Filtro por agencia
        agency = self.request.query_params.get('agency')
        if agency:
            queryset = queryset.filter(agency_s__icontains=agency)
        
        # Búsqueda por nombre
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(agency_s__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['get'], url_path='presentations')
    def presentations(self, request, pk=None):
        """
        Retorna todas las presentaciones de un speaker específico.
        
        GET /api/eventos/speakers/5/presentations/
        """
        speaker = self.get_object()
        presentations = speaker.presentations.all()
        serializer = PresentationDetailSerializer(presentations, many=True)
        return Response(serializer.data)


# ============== VIEWSETS PARA RELACIONES ==============

class PresentationSpeakerViewSet(viewsets.ViewSet):
    """
    ViewSet para gestionar la relación entre presentaciones y speakers.
    """
    permission_classes = [AllowAny]
    
    def create(self, request):
        """
        Asocia un speaker a una presentación.
        
        POST /api/eventos/presentation-speakers/
        Body: {"presentation_id": 1, "speaker_id": 2}
        """
        presentation_id = request.data.get('presentation_id')
        speaker_id = request.data.get('speaker_id')
        
        if not presentation_id or not speaker_id:
            return Response(
                {"error": "Se requieren presentation_id y speaker_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            speaker = Speaker.objects.get(id=speaker_id)
        except Presentation.DoesNotExist:
            return Response(
                {"error": f"Presentación con id {presentation_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Speaker.DoesNotExist:
            return Response(
                {"error": f"Speaker con id {speaker_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        relation, created = PresentationSpeaker.objects.get_or_create(
            id_presentation=presentation,
            id_speaker=speaker
        )
        
        if created:
            return Response(
                {"message": "Speaker asociado exitosamente"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "La relación ya existe"},
                status=status.HTTP_200_OK
            )
    
    def destroy(self, request, pk=None):
        """
        Elimina la asociación entre presentación y speaker.
        
        DELETE /api/eventos/presentation-speakers/5-10/
        pk debe ser en formato: presentation_id-speaker_id
        """
        try:
            presentation_id, speaker_id = pk.split('-')
            relation = PresentationSpeaker.objects.get(
                id_presentation_id=presentation_id,
                id_speaker_id=speaker_id
            )
            relation.delete()
            return Response(
                {"message": "Relación eliminada exitosamente"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ValueError:
            return Response(
                {"error": "Formato incorrecto. Use: presentation_id-speaker_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PresentationSpeaker.DoesNotExist:
            return Response(
                {"error": "Relación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )