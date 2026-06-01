"""
views.py  —  FELA application ViewSets

Changes from previous version:
- All ViewSets now use OwnershipMixin (replaces DeleteOnlySuperuser)
- perform_create() is handled by OwnershipMixin (assigns request.user as created_by)
- All field references updated to new model conventions
- Filters, orderings and related queries updated accordingly
"""

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
from .mixins import OwnershipMixin


# ===========================================================================
# COUNTRY
# ===========================================================================

class CountryViewSet(OwnershipMixin, viewsets.ModelViewSet):
    """
    ViewSet for countries.
    - GET: public
    - POST: authenticated + approved user
    - PUT/PATCH/DELETE: record owner or superuser
    """
    queryset = Country.objects.all()
    lookup_field = 'pk'
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
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(country__icontains=search)
        return queryset

    def perform_destroy(self, instance):
        cities_count = instance.cities.count()
        if cities_count > 0:
            raise ValidationError({
                'detail': f"Cannot delete country '{instance.country}'. It has {cities_count} related city(ies).",
                'cities_count': cities_count
            })
        events_count = instance.events_country_e.count()
        if events_count > 0:
            raise ValidationError({
                'detail': f"Cannot delete country '{instance.country}'. It has {events_count} related event(s).",
                'events_count': events_count
            })
        speakers_count = instance.speaker_country.count()
        if speakers_count > 0:
            raise ValidationError({
                'detail': f"Cannot delete country '{instance.country}'. It has {speakers_count} related speaker(s).",
                'speakers_count': speakers_count
            })
        instance.delete()


# ===========================================================================
# CITY
# ===========================================================================

class CityViewSet(OwnershipMixin, viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
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
        events_count = Event.objects.filter(
            country=instance.country,
            city=instance.city
        ).count()
        if events_count > 0:
            raise ValidationError({
                'detail': f"Cannot delete city '{instance.city}'. It has {events_count} related event(s).",
                'events_count': events_count
            })
        instance.delete()


# ===========================================================================
# AGENCY
# ===========================================================================

class AgencyViewSet(OwnershipMixin, viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        queryset = Agency.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def perform_destroy(self, instance):
        events_count = instance.events_agencies.count()
        if events_count > 0:
            raise ValidationError({
                'detail': f"Cannot delete agency '{instance.name}'. It has {events_count} related event(s).",
                'events_count': events_count
            })
        instance.delete()


# ===========================================================================
# EVENT
# ===========================================================================

class EventViewSet(OwnershipMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['event_title']
    filterset_fields = ['year', 'type', 'country__country']
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
        queryset = Event.objects.select_related('country').prefetch_related(
            'presentations_event', 'agency'
        ).all()
        year = self.request.query_params.get('year')
        country = self.request.query_params.get('country')
        event_type = self.request.query_params.get('type')
        search = self.request.query_params.get('search')
        if year:
            queryset = queryset.filter(year=year)
        if country:
            queryset = queryset.filter(country__country__iexact=country)
        if event_type:
            queryset = queryset.filter(type__icontains=event_type)
        if search:
            queryset = queryset.filter(event_title__icontains=search)
        return queryset

    def perform_destroy(self, instance):
        # CASCADE handles presentations and relations automatically
        instance.delete()

    @action(detail=False, methods=['post'], url_path='create-complete')
    def create_complete(self, request):
        """Creates a complete event with nested presentations and speakers."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Inject created_by — client cannot supply this value
            event = serializer.save(created_by=request.user)
            return Response(
                EventDetailSerializer(event).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='add-agency')
    def add_agency(self, request, pk=None):
        """Adds an agency to an existing event."""
        event = self.get_object()  # triggers has_object_permission
        serializer = EventAgencySerializer(data=request.data)
        if serializer.is_valid():
            agency_id = serializer.validated_data.get('agency_id')
            agency_name = serializer.validated_data.get('agency_name')
            if agency_id:
                try:
                    agency = Agency.objects.get(id=agency_id)
                except Agency.DoesNotExist:
                    return Response(
                        {"error": f"Agency with id {agency_id} does not exist."},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                agency = Agency.objects.filter(name__iexact=agency_name).first()
                if not agency:
                    agency = Agency.objects.create(
                        name=agency_name,
                        created_by=request.user
                    )
            relation, created = EventAgency.objects.get_or_create(
                event=event,
                agency=agency,
                defaults={'created_by': request.user}
            )
            if created:
                return Response(
                    {"message": f"Agency '{agency.name}' added.", "agency": AgencySerializer(agency).data},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {"message": f"Agency '{agency.name}' was already associated.", "agency": AgencySerializer(agency).data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove-agency')
    def remove_agency(self, request, pk=None):
        """Removes an agency from an event."""
        event = self.get_object()  # triggers has_object_permission
        serializer = EventAgencySerializer(data=request.data)
        if serializer.is_valid():
            agency_id = serializer.validated_data.get('agency_id')
            agency_name = serializer.validated_data.get('agency_name')
            if agency_id:
                try:
                    agency = Agency.objects.get(id=agency_id)
                except Agency.DoesNotExist:
                    return Response({"error": f"Agency {agency_id} not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                agency = Agency.objects.filter(name__iexact=agency_name).first()
                if not agency:
                    return Response({"error": f"Agency '{agency_name}' not found."}, status=status.HTTP_404_NOT_FOUND)
            try:
                relation = EventAgency.objects.get(event=event, agency=agency)
                relation.delete()
                return Response({"message": f"Agency '{agency.name}' removed."}, status=status.HTTP_200_OK)
            except EventAgency.DoesNotExist:
                return Response({"error": f"Agency '{agency.name}' is not associated with this event."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put', 'patch'], url_path='agencies')
    @transaction.atomic
    def update_agencies(self, request, pk=None):
        """Replaces all agencies of an event."""
        event = self.get_object()  # triggers has_object_permission
        serializer = EventAgenciesUpdateSerializer(data=request.data)
        if serializer.is_valid():
            agencies_ids = serializer.validated_data.get('agencies')
            agency_names = serializer.validated_data.get('agency_names')
            EventAgency.objects.filter(event=event).delete()
            if agencies_ids:
                for agency_id in agencies_ids:
                    try:
                        agency = Agency.objects.get(id=agency_id)
                        EventAgency.objects.create(event=event, agency=agency, created_by=request.user)
                    except Agency.DoesNotExist:
                        pass
            elif agency_names:
                for agency_name in agency_names:
                    agency = Agency.objects.filter(name__iexact=agency_name).first()
                    if not agency:
                        agency = Agency.objects.create(name=agency_name, created_by=request.user)
                    EventAgency.objects.create(event=event, agency=agency, created_by=request.user)
            return Response(EventDetailSerializer(event).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='agencies')
    def list_agencies(self, request, pk=None):
        event = self.get_object()
        agencies = event.agency.all()
        return Response(AgencySerializer(agencies, many=True).data)


# ===========================================================================
# PRESENTATION
# ===========================================================================

class PresentationViewSet(OwnershipMixin, viewsets.ModelViewSet):
    queryset = Presentation.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'event__year']
    ordering = ['-event__year']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'search']:
            return PresentationDetailSerializer
        return PresentationSerializer

    def get_queryset(self):
        return Presentation.objects.select_related(
            'event',
            'event__country'
        ).prefetch_related('speakers').all()

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        queryset = self.get_queryset()
        event_id = request.query_params.get('event_id')
        event_title = request.query_params.get('event_title')
        if event_id:
            queryset = queryset.filter(event__id=event_id)
        if event_title:
            queryset = queryset.filter(event__event_title__icontains=event_title)
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
            queryset = queryset.filter(event__country__country__iexact=country)
        year = request.query_params.get('year')
        if year:
            queryset = queryset.filter(event__year=year)
        agency = request.query_params.get('agency')
        if agency:
            queryset = queryset.filter(event__agency__name__icontains=agency)
        queryset = queryset.distinct()
        serializer = PresentationDetailSerializer(queryset, many=True)
        return Response(serializer.data)


# ===========================================================================
# SPEAKER
# ===========================================================================

class SpeakerViewSet(OwnershipMixin, viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['country__country']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SpeakerDetailSerializer
        return SpeakerSerializer

    def get_queryset(self):
        queryset = Speaker.objects.select_related('country', 'agency').all()
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country__country__iexact=country)
        agency = self.request.query_params.get('agency')
        if agency:
            queryset = queryset.filter(agency__name__icontains=agency)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(agency__name__icontains=search)
            )
        return queryset

    def perform_destroy(self, instance):
        presentations_count = instance.presentations.count()
        if presentations_count > 0:
            raise ValidationError({
                'detail': f"Cannot delete speaker '{instance.name}'. Has {presentations_count} related presentation(s).",
                'presentations_count': presentations_count
            })
        instance.delete()

    @action(detail=True, methods=['get'], url_path='presentations')
    def presentations(self, request, pk=None):
        speaker = self.get_object()
        presentations = speaker.presentations.all()
        return Response(PresentationDetailSerializer(presentations, many=True).data)


# ===========================================================================
# PRESENTATION SPEAKER  (relation ViewSet)
# ===========================================================================

class PresentationSpeakerViewSet(OwnershipMixin, viewsets.ViewSet):

    def create(self, request):
        presentation_id = request.data.get('presentation_id')
        speaker_id = request.data.get('speaker_id')
        if not presentation_id or not speaker_id:
            return Response(
                {"error": "presentation_id and speaker_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            presentation = Presentation.objects.get(id=presentation_id)
            speaker = Speaker.objects.get(id=speaker_id)
        except Presentation.DoesNotExist:
            return Response({"error": f"Presentation {presentation_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Speaker.DoesNotExist:
            return Response({"error": f"Speaker {speaker_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        relation, created = PresentationSpeaker.objects.get_or_create(
            presentation=presentation,
            speaker=speaker,
            defaults={'created_by': request.user}  # ownership assigned here
        )
        if created:
            return Response({"message": "Speaker linked to presentation."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Relation already exists."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            presentation_id, speaker_id = pk.split('-')
            relation = PresentationSpeaker.objects.get(
                presentation_id=presentation_id,
                speaker_id=speaker_id
            )
            self.check_object_permissions(request, relation)
            relation.delete()
            return Response({"message": "Relation deleted."}, status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"error": "Use format: presentation_id-speaker_id"}, status=status.HTTP_400_BAD_REQUEST)
        except PresentationSpeaker.DoesNotExist:
            return Response({"error": "Relation not found."}, status=status.HTTP_404_NOT_FOUND)


# ===========================================================================
# EVENT AGENCY  (relation ViewSet)
# ===========================================================================

class EventAgencyViewSet(OwnershipMixin, viewsets.ViewSet):

    def create(self, request):
        event_id = request.data.get('event_id')
        agency_id = request.data.get('agency_id')
        if not event_id or not agency_id:
            return Response({"error": "event_id and agency_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            event = Event.objects.get(id=event_id)
            agency = Agency.objects.get(id=agency_id)
        except Event.DoesNotExist:
            return Response({"error": f"Event {event_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except Agency.DoesNotExist:
            return Response({"error": f"Agency {agency_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        relation, created = EventAgency.objects.get_or_create(
            event=event,
            agency=agency,
            defaults={'created_by': request.user}
        )
        if created:
            return Response({"message": "Agency linked to event."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Relation already exists."}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            event_id, agency_id = pk.split('-')
            relation = EventAgency.objects.get(event_id=event_id, agency_id=agency_id)
            self.check_object_permissions(request, relation)
            relation.delete()
            return Response({"message": "Relation deleted."}, status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response({"error": "Use format: event_id-agency_id"}, status=status.HTTP_400_BAD_REQUEST)
        except EventAgency.DoesNotExist:
            return Response({"error": "Relation not found."}, status=status.HTTP_404_NOT_FOUND)