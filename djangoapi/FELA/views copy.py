from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

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
from .permissions import DeleteOnlySuperuser


# ============== VIEWSETS BÁSICOS ==============

class CountryViewSet(viewsets.ModelViewSet):
#    """
#    ViewSet para países.
#    GET: Todos los usuarios
#    POST/PUT/PATCH: Usuarios autenticados
#    DELETE: Solo superusuarios
#    """
    """

    The get and post methods are defined in the BaseDjangoView. They forward the request
    to the methods selectone, selectall, insert, update, and delete, depending of the 
    action parameter in the URL.

    This class redefine the the methods selectone, selectall, insert, update, and delete
    of the BaseDjangoView class to add a new action, insert2.
  
    To use this view:
    To get a record, the URL must be like:
        GET /FELA_view/selectone/<id>/
    To get all the records, the URL must be like:
        GET /FELA_view/selectall/
    To insert a record, the URL must be like:
        POST /FELA_view/insert/ --> The data must be sent in the body of the request.
    To update a record, the URL must be like:
        POST /FELA_view/update/<id>/ --> The data must be sent in the body of the request.
    To delete a record, the URL must be like:
        POST /FELA_view/delete/<id>/
    """
        
    queryset = Country.objects.all()
    permission_classes = [DeleteOnlySuperuser]
    lookup_field = 'country'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CountryDetailSerializer
        return CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ciudades.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [DeleteOnlySuperuser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country__country']

    def get_queryset(self):
        queryset = City.objects.select_related('country').all()
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country__country=country)
        return queryset


class AgencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para agencias.
    """
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [DeleteOnlySuperuser]


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet para eventos.
    Incluye acción custom para crear evento completo.
    """
    queryset = Event.objects.all()
    permission_classes = [DeleteOnlySuperuser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year', 'type', 'country_e__country']

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
        
        if year:
            queryset = queryset.filter(year=year)
        if country:
            queryset = queryset.filter(country_e__country=country)
        if event_type:
            queryset = queryset.filter(type=event_type)
            
        return queryset

    @action(detail=False, methods=['post'], url_path='create-complete')
    def create_complete(self, request):
        """
        Crea un evento completo con presentaciones y speakers en una sola operación.
        
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
                    "language": "en",
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
    ViewSet para presentaciones.
    Incluye búsqueda compleja con múltiples filtros.
    """
    queryset = Presentation.objects.all()
    permission_classes = [DeleteOnlySuperuser]

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
        
        Ejemplo: /api/presentations/search/?language=es&country=España&year=2025
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
            queryset = queryset.filter(language__iexact=language)

        # Filtro por país del evento
        country = request.query_params.get('country')
        if country:
            queryset = queryset.filter(event_title__country_e__country=country)

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
    ViewSet para speakers.
    """
    queryset = Speaker.objects.all()
    permission_classes = [DeleteOnlySuperuser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country_s__country', 'agency_s']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpeakerDetailSerializer
        return SpeakerSerializer

    def get_queryset(self):
        queryset = Speaker.objects.select_related('country_s').all()
        
        # Filtros adicionales
        country = self.request.query_params.get('country')
        agency = self.request.query_params.get('agency')
        
        if country:
            queryset = queryset.filter(country_s__country=country)
        if agency:
            queryset = queryset.filter(agency_s__icontains=agency)
            
        return queryset

    @action(detail=True, methods=['get'], url_path='presentations')
    def presentations(self, request, pk=None):
        """
        Retorna todas las presentaciones de un speaker específico.
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request):
        """
        Asocia un speaker a una presentación.
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
        pk debe ser en formato: presentation_id-speaker_id
        Ejemplo: /api/presentation-speakers/5-10/
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