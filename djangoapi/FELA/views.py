from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from django.db import transaction

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
    SpeakerSerializer, SpeakerDetailSerializer,
    EventAgencySerializer, EventAgenciesUpdateSerializer
)
from .permissions import DeleteOnlySuperuser


# ============== VIEWSETS CON PERMISOS Y VALIDACIÓN DELETE ==============

class CountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para países con búsqueda (autocomplete).
    
    Permisos:
    - GET: Público
    - POST/PUT/PATCH: Usuario autenticado y aprobado
    - DELETE: Solo superusuario
    """
    queryset = Country.objects.all()
    permission_classes = [DeleteOnlySuperuser]
    lookup_field = 'country'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['country']
    ordering_fields = ['country']
    ordering = ['country']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CountryDetailSerializer
        return CountrySerializer
    
    def get_queryset(self):
        queryset = Country.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(country__icontains=search)
        return queryset
    
    def perform_destroy(self, instance):
        """
        Validar antes de eliminar.
        No permitir si tiene ciudades o eventos relacionados.
        """
        # Verificar ciudades
        cities_count = instance.cities.count()
        if cities_count > 0:
            raise ValidationError({
                'detail': f"No se puede eliminar el país '{instance.country}'. Tiene {cities_count} ciudad(es) relacionada(s).",
                'cities_count': cities_count
            })
        
        # Verificar eventos
        events_count = instance.events.count()
        if events_count > 0:
            raise ValidationError({
                'detail': f"No se puede eliminar el país '{instance.country}'. Tiene {events_count} evento(s) relacionado(s).",
                'events_count': events_count
            })
        
        # Verificar speakers
        speakers_count = instance.speakers.count()
        if speakers_count > 0:
            raise ValidationError({
                'detail': f"No se puede eliminar el país '{instance.country}'. Tiene {speakers_count} speaker(s) relacionado(s).",
                'speakers_count': speakers_count
            })
        
        # Si no hay dependencias, eliminar
        instance.delete()


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ciudades con búsqueda y filtro por país.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [DeleteOnlySuperuser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['city']
    filterset_fields = ['country__country']
    ordering_fields = ['city', 'country']
    ordering = ['country__country', 'city']
    
    def get_queryset(self):
        queryset = City.objects.select_related('country').all()
        
        country_param = self.request.query_params.get('country')
        if country_param:
            queryset = queryset.filter(country__country__iexact=country_param)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(city__icontains=search)
        
        return queryset
    
    def perform_destroy(self, instance):
        """
        Validar antes de eliminar.
        No permitir si hay eventos en esta ciudad.
        """
        # Verificar si hay eventos en esta ciudad
        events_count = Event.objects.filter(
            country_e=instance.country,
            city_e=instance.city
        ).count()
        
        if events_count > 0:
            raise ValidationError({
                'detail': f"No se puede eliminar la ciudad '{instance.city}'. Tiene {events_count} evento(s) relacionado(s).",
                'events_count': events_count
            })
        
        instance.delete()


class AgencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para agencias con búsqueda (autocomplete).
    """
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [DeleteOnlySuperuser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    ordering = ['nombre']
    
    def get_queryset(self):
        queryset = Agency.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset
    
    def perform_destroy(self, instance):
        """
        Validar antes de eliminar.
        No permitir si hay eventos relacionados.
        """
        events_count = instance.events.count()
        if events_count > 0:
            raise ValidationError({
                'detail': f"No se puede eliminar la agencia '{instance.nombre}'. Tiene {events_count} evento(s) relacionado(s).",
                'events_count': events_count
            })
        
        instance.delete()


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet para eventos con búsqueda por título.
    """
    queryset = Event.objects.all()
    permission_classes = [DeleteOnlySuperuser]
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
        elif self.action in ['add_agency', 'remove_agency']:
            return EventAgencySerializer
        elif self.action == 'update_agencies':
            return EventAgenciesUpdateSerializer
        return EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.select_related('country_e').prefetch_related(
            'presentations', 'agencies'
        ).all()
        
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
    
    def perform_destroy(self, instance):
        """
        Validar antes de eliminar.
        Advertir sobre cascada de presentaciones.
        """
        presentations_count = instance.presentations.count()
        
        if presentations_count > 0:
            # Informar pero permitir (CASCADE configurado en BD)
            # El usuario superusuario es consciente de esto
            pass
        
        # Eliminar (CASCADE se encarga de presentations y relaciones)
        instance.delete()
    
    @action(detail=False, methods=['post'], url_path='create-complete')
    def create_complete(self, request):
        """Crea un evento completo con presentaciones y speakers."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            return Response(
                EventDetailSerializer(event).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='add-agency')
    def add_agency(self, request, pk=None):
        """Agrega una agencia a un evento existente."""
        event = self.get_object()
        serializer = EventAgencySerializer(data=request.data)
        
        if serializer.is_valid():
            agency_id = serializer.validated_data.get('agency_id')
            agency_name = serializer.validated_data.get('agency_name')
            
            if agency_id:
                try:
                    agency = Agency.objects.get(id=agency_id)
                except Agency.DoesNotExist:
                    return Response(
                        {"error": f"Agencia con ID {agency_id} no existe."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                agency = Agency.objects.filter(nombre__iexact=agency_name).first()
                if not agency:
                    agency = Agency.objects.create(nombre=agency_name)
            
            relation, created = EventAgency.objects.get_or_create(
                id_event=event,
                id_agencia=agency
            )
            
            if created:
                return Response(
                    {
                        "message": f"Agencia '{agency.nombre}' agregada exitosamente al evento.",
                        "agency": AgencySerializer(agency).data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "message": f"La agencia '{agency.nombre}' ya está asociada a este evento.",
                        "agency": AgencySerializer(agency).data
                    },
                    status=status.HTTP_200_OK
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='remove-agency')
    def remove_agency(self, request, pk=None):
        """Elimina una agencia de un evento."""
        event = self.get_object()
        serializer = EventAgencySerializer(data=request.data)
        
        if serializer.is_valid():
            agency_id = serializer.validated_data.get('agency_id')
            agency_name = serializer.validated_data.get('agency_name')
            
            if agency_id:
                try:
                    agency = Agency.objects.get(id=agency_id)
                except Agency.DoesNotExist:
                    return Response(
                        {"error": f"Agencia con ID {agency_id} no existe."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                agency = Agency.objects.filter(nombre__iexact=agency_name).first()
                if not agency:
                    return Response(
                        {"error": f"Agencia '{agency_name}' no existe."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            
            try:
                relation = EventAgency.objects.get(id_event=event, id_agencia=agency)
                relation.delete()
                return Response(
                    {"message": f"Agencia '{agency.nombre}' eliminada del evento."},
                    status=status.HTTP_200_OK
                )
            except EventAgency.DoesNotExist:
                return Response(
                    {"error": f"La agencia '{agency.nombre}' no está asociada a este evento."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put', 'patch'], url_path='agencies')
    @transaction.atomic
    def update_agencies(self, request, pk=None):
        """Reemplaza todas las agencias de un evento."""
        event = self.get_object()
        serializer = EventAgenciesUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            agencies_ids = serializer.validated_data.get('agencies')
            agency_names = serializer.validated_data.get('agency_names')
            
            EventAgency.objects.filter(id_event=event).delete()
            
            if agencies_ids:
                for agency_id in agencies_ids:
                    try:
                        agency = Agency.objects.get(id=agency_id)
                        EventAgency.objects.create(id_event=event, id_agencia=agency)
                    except Agency.DoesNotExist:
                        pass
            
            elif agency_names:
                for agency_name in agency_names:
                    agency = Agency.objects.filter(nombre__iexact=agency_name).first()
                    if not agency:
                        agency = Agency.objects.create(nombre=agency_name)
                    EventAgency.objects.create(id_event=event, id_agencia=agency)
            
            return Response(
                EventDetailSerializer(event).data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='agencies')
    def list_agencies(self, request, pk=None):
        """Lista todas las agencias de un evento."""
        event = self.get_object()
        agencies = event.agencies.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data)


class PresentationViewSet(viewsets.ModelViewSet):
    """ViewSet para presentaciones con búsqueda compleja."""
    queryset = Presentation.objects.all()
    permission_classes = [DeleteOnlySuperuser]
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
    
    def perform_destroy(self, instance):
        """
        Validar antes de eliminar.
        Advertir sobre cascada de relaciones con speakers.
        """
        speakers_count = instance.speakers.count()
        # Informar pero permitir (CASCADE configurado)
        instance.delete()
    
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """Búsqueda compleja de presentaciones con múltiples filtros."""
        queryset = self.get_queryset()
        
        event_id = request.query_params.get('event_id')
        event_title = request.query_params.get('event_title')
        if event_id:
            queryset = queryset.filter(event_title__id=event_id)
        if event_title:
            queryset = queryset.filter(event_title__event_title__icontains=event_title)
        
        speaker_id = request.query_params.get('speaker_id')
        speaker_name = request.query_params.get('speaker_name')
        if speaker_id:
            queryset = queryset.filter(speakers__id=speaker_id)
        if speaker_name:
            queryset = queryset.filter(speakers__name__icontains=speaker_name)
        
        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(language__contains=[language])
        
        country = request.query_params.get('country')
        if country:
            queryset = queryset.filter(event_title__country_e__country__iexact=country)
        
        year = request.query_params.get('year')
        if year:
            queryset = queryset.filter(event_title__year=year)
        
        agency = request.query_params.get('agency')
        if agency:
            queryset = queryset.filter(
                event_title__agencies__nombre__icontains=agency
            )
        
        queryset = queryset.distinct()
        
        serializer = PresentationDetailSerializer(queryset, many=True)
        return Response(serializer.data)


class SpeakerViewSet(viewsets.ModelViewSet):
    """ViewSet para speakers con búsqueda."""
    queryset = Speaker.objects.all()
    permission_classes = [DeleteOnlySuperuser]
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
        
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country_s__country__iexact=country)
        
        agency = self.request.query_params.get('agency')
        if agency:
            queryset = queryset.filter(agency_s__icontains=agency)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(agency_s__icontains=search)
            )
        
        return queryset
    
    def perform_destroy(self, instance):
        """
        Validar antes de eliminar.
        No permitir si tiene presentaciones relacionadas.
        """
        presentations_count = instance.presentations.count()
        if presentations_count > 0:
            raise ValidationError({
                'detail': f"No se puede eliminar el speaker '{instance.name}'. Tiene {presentations_count} presentación(es) relacionada(s).",
                'presentations_count': presentations_count
            })
        
        instance.delete()
    
    @action(detail=True, methods=['get'], url_path='presentations')
    def presentations(self, request, pk=None):
        """Retorna todas las presentaciones de un speaker específico."""
        speaker = self.get_object()
        presentations = speaker.presentations.all()
        serializer = PresentationDetailSerializer(presentations, many=True)
        return Response(serializer.data)


# ============== VIEWSETS PARA RELACIONES ==============

class PresentationSpeakerViewSet(viewsets.ViewSet):
    """ViewSet para gestionar la relación entre presentaciones y speakers."""
    permission_classes = [DeleteOnlySuperuser]
    
    def create(self, request):
        """Asocia un speaker a una presentación."""
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
        """Elimina la asociación entre presentación y speaker."""
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


class EventAgencyViewSet(viewsets.ViewSet):
    """ViewSet genérico para gestionar relación events-agencies."""
    permission_classes = [DeleteOnlySuperuser]
    
    def create(self, request):
        """Asocia una agencia a un evento."""
        event_id = request.data.get('event_id')
        agency_id = request.data.get('agency_id')
        
        if not event_id or not agency_id:
            return Response(
                {"error": "Se requieren event_id y agency_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            event = Event.objects.get(id=event_id)
            agency = Agency.objects.get(id=agency_id)
        except Event.DoesNotExist:
            return Response(
                {"error": f"Evento con id {event_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Agency.DoesNotExist:
            return Response(
                {"error": f"Agencia con id {agency_id} no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        relation, created = EventAgency.objects.get_or_create(
            id_event=event,
            id_agencia=agency
        )
        
        if created:
            return Response(
                {"message": "Agencia asociada al evento exitosamente"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "La relación ya existe"},
                status=status.HTTP_200_OK
            )
    
    def destroy(self, request, pk=None):
        """Elimina la asociación entre evento y agencia."""
        try:
            event_id, agency_id = pk.split('-')
            relation = EventAgency.objects.get(
                id_event_id=event_id,
                id_agencia_id=agency_id
            )
            relation.delete()
            return Response(
                {"message": "Relación eliminada exitosamente"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ValueError:
            return Response(
                {"error": "Formato incorrecto. Use: event_id-agency_id"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EventAgency.DoesNotExist:
            return Response(
                {"error": "Relación no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )