"""
serializers.py  —  FELA application serializers

Changes from previous version:
- All field names updated to match new model conventions
  (nombre→name, country_e→country, city_e→city, country_s→country,
   agency_s→agency, id_event→event, id_agencia→agency,
   id_presentation→presentation, id_speaker→speaker,
   event_title FK→event FK by id)
- created_by added as SerializerMethodField (read-only, never writable by client)
- EventCompleteCreateSerializer.create() propagates created_by to all sub-objects
"""

from rest_framework import serializers
from django.db import transaction
from .models import (
    Country, City, Agency, Event, Presentation,
    Speaker, PresentationSpeaker, EventAgency
)


# ===========================================================================
# HELPERS
# ===========================================================================

def _get_created_by_username(obj):
    """Returns the username of the record creator, or None for legacy records."""
    if obj.created_by:
        return obj.created_by.username
    return None


# ===========================================================================
# LEVEL 1 — BASIC SERIALIZERS (create / update)
# ===========================================================================

class CountrySerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'country', 'lat', 'lon', 'created_by', 'created_at']

    def get_created_by(self, obj):
        return _get_created_by_username(obj)

    def validate(self, data):
        lat = data.get('lat')
        lon = data.get('lon')
        # On PATCH, only one coordinate may be present — skip validation
        # if neither is provided or if this is a partial update with only one.
        if lat is None and lon is None:
            return data
        # On full create (POST), both must be present
        if not self.partial and (lat is None or lon is None):
            raise serializers.ValidationError({
                'coordinates': 'Coordinates (lat, lon) are required.'
            })
        return data

    def create(self, validated_data):
        country_name = validated_data['country']
        existing = Country.objects.filter(country__iexact=country_name).first()
        if existing:
            new_lat = validated_data.get('lat')
            new_lon = validated_data.get('lon')
            if new_lat and new_lon and not (new_lat == 0 and new_lon == 0):
                existing.lat = new_lat
                existing.lon = new_lon
                existing.save()
            return existing
        return Country.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.save()
        return instance


class CitySerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'country', 'city', 'lat', 'lon', 'created_by', 'created_at']

    def get_created_by(self, obj):
        return _get_created_by_username(obj)

    def validate_country(self, value):
        if not Country.objects.filter(country__iexact=value).exists():
            raise serializers.ValidationError(
                f"Country '{value}' does not exist. Create it first."
            )
        return value

    def validate(self, data):
        lat = data.get('lat')
        lon = data.get('lon')
        # On PATCH, skip coordinate validation if neither is provided
        if lat is None and lon is None:
            return data
        # On full create (POST), both must be present
        if not self.partial and (lat is None or lon is None):
            raise serializers.ValidationError({
                'coordinates': 'Coordinates (lat, lon) are required.'
            })
        return data

    def create(self, validated_data):
        country_name = validated_data.pop('country')
        country = Country.objects.filter(country__iexact=country_name).first()
        existing = City.objects.filter(
            country=country, city__iexact=validated_data['city']
        ).first()
        if existing:
            if validated_data.get('lat') and validated_data.get('lon'):
                existing.lat = validated_data['lat']
                existing.lon = validated_data['lon']
                existing.save()
            return existing
        return City.objects.create(country=country, **validated_data)

    def update(self, instance, validated_data):
        instance.lat = validated_data.get('lat', instance.lat)
        instance.lon = validated_data.get('lon', instance.lon)
        instance.save()
        return instance


class AgencySerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Agency
        fields = ['id', 'name', 'long_name', 'created_by', 'created_at']

    def get_created_by(self, obj):
        return _get_created_by_username(obj)

    def create(self, validated_data):
        existing = Agency.objects.filter(name__iexact=validated_data['name']).first()
        if existing:
            return existing
        return Agency.objects.create(**validated_data)


class SpeakerSerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    agency = serializers.CharField(required=False, allow_blank=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Speaker
        fields = ['id', 'name', 'country', 'agency', 'created_by', 'created_at']

    def get_created_by(self, obj):
        return _get_created_by_username(obj)

    def validate_country(self, value):
        if not Country.objects.filter(country__iexact=value).exists():
            raise serializers.ValidationError(
                f"Country '{value}' does not exist."
            )
        return value

    def create(self, validated_data):
        country_name = validated_data.pop('country')
        agency_name = validated_data.pop('agency', '')
        country = Country.objects.filter(country__iexact=country_name).first()
        agency = None
        if agency_name:
            agency, _ = Agency.objects.get_or_create(name=agency_name)

        existing = Speaker.objects.filter(
            name__iexact=validated_data['name'],
            country=country
        ).first()
        if existing:
            if agency and existing.agency != agency:
                existing.agency = agency
                existing.save()
            return existing

        return Speaker.objects.create(
            country=country,
            agency=agency,
            **validated_data
        )

    def update(self, instance, validated_data):
        country_name = validated_data.pop('country', None)
        agency_name = validated_data.pop('agency', None)

        if country_name:
            new_country = Country.objects.filter(country__iexact=country_name).first()
            if not new_country:
                raise serializers.ValidationError({'country': f"Country '{country_name}' does not exist."})
            instance.country = new_country

        if agency_name is not None:
            if agency_name:
                agency, _ = Agency.objects.get_or_create(name=agency_name)
                instance.agency = agency
            else:
                instance.agency = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    # required=False so that PATCH requests that omit 'country' do not fail
    # field-level validation before reaching validate().
    country = serializers.CharField(required=False)
    agency = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Agency.objects.all(),
        required=False
    )
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'date', 'year', 'type',
            'country', 'city', 'event_title',
            'agency', 'created_by', 'created_at'
        ]

    def get_created_by(self, obj):
        return _get_created_by_username(obj)

    def validate(self, data):
        # On PATCH, country and/or city may be absent — only validate when present.
        country_name = data.get('country')
        city_name = data.get('city')

        # Nothing geography-related in this payload → skip validation
        if not country_name and not city_name:
            return data

        # If only city is provided without country, resolve country from instance
        if city_name and not country_name:
            instance = getattr(self, 'instance', None)
            if instance:
                country_name = instance.country.country

        if country_name:
            country = Country.objects.filter(country__iexact=country_name).first()
            if not country:
                raise serializers.ValidationError(
                    {'country': f"Country '{country_name}' does not exist."}
                )
            # Validate city only when both are present
            if city_name:
                city = City.objects.filter(country=country, city__iexact=city_name).first()
                if not city:
                    raise serializers.ValidationError(
                        {'city': f"City '{city_name}' does not exist in '{country.country}'."}
                    )
        return data

    @transaction.atomic
    def create(self, validated_data):
        agencies_data = validated_data.pop('agency', [])
        country_name = validated_data.pop('country')
        country = Country.objects.filter(country__iexact=country_name).first()
        event = Event.objects.create(country=country, **validated_data)
        for ag in agencies_data:
            EventAgency.objects.create(event=event, agency=ag)
        return event

    @transaction.atomic
    def update(self, instance, validated_data):
        agencies_data = validated_data.pop('agency', None)
        country_name = validated_data.pop('country', None)
        if country_name:
            country = Country.objects.filter(country__iexact=country_name).first()
            instance.country = country
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if agencies_data is not None:
            EventAgency.objects.filter(event=instance).delete()
            for ag in agencies_data:
                EventAgency.objects.create(event=instance, agency=ag)
        return instance


class PresentationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    language = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'event',
            'language', 'url_document', 'observations',
            'created_by', 'created_at'
        ]

    def get_created_by(self, obj):
        return _get_created_by_username(obj)


# ===========================================================================
# LEVEL 2 — READ-ONLY NESTED SERIALIZERS
# ===========================================================================

class CountryDetailSerializer(serializers.ModelSerializer):
    cities_count = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'country', 'lat', 'lon', 'cities_count', 'created_by', 'created_at']

    def get_cities_count(self, obj):
        return obj.cities.count()

    def get_created_by(self, obj):
        return _get_created_by_username(obj)


class SpeakerDetailSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.country')
    agency = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Speaker
        fields = ['id', 'name', 'country', 'agency', 'created_by']

    def get_agency(self, obj):
        return obj.agency.name if obj.agency else None

    def get_created_by(self, obj):
        return _get_created_by_username(obj)


class PresentationDetailSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.event_title')
    event_id = serializers.IntegerField(source='event.id')
    event_country = serializers.CharField(source='event.country.country')
    event_city = serializers.CharField(source='event.city')
    event_year = serializers.IntegerField(source='event.year')
    speakers = SpeakerDetailSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'language', 'url_document', 'observations',
            'event_id', 'event_title', 'event_country', 'event_city',
            'event_year', 'speakers', 'created_by', 'created_at'
        ]

    def get_created_by(self, obj):
        return _get_created_by_username(obj)


class EventDetailSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.country')
    country_lat = serializers.DecimalField(
        source='country.lat', max_digits=10, decimal_places=7, read_only=True
    )
    country_lon = serializers.DecimalField(
        source='country.lon', max_digits=10, decimal_places=7, read_only=True
    )
    presentations = PresentationSerializer(
        source='presentations_event', many=True, read_only=True
    )
    agencies = AgencySerializer(source='agency', many=True, read_only=True)
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'date', 'year', 'type',
            'country', 'city', 'event_title',
            'country_lat', 'country_lon',
            'presentations', 'agencies',
            'created_by', 'created_at'
        ]

    def get_created_by(self, obj):
        return _get_created_by_username(obj)


# ===========================================================================
# LEVEL 3 — COMPLEX WRITE SERIALIZERS
# ===========================================================================

class SpeakerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=100)
    agency = serializers.CharField(max_length=150, required=False, allow_blank=True)


class PresentationCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    language = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    url = serializers.CharField(required=False, allow_blank=True)
    observations = serializers.CharField(required=False, allow_blank=True)
    speakers = SpeakerCreateSerializer(many=True, required=False)


class EventCompleteCreateSerializer(serializers.Serializer):
    """
    Creates a complete event with nested presentations and speakers
    in a single atomic operation.
    
    created_by is NOT accepted from the client; it is injected by the
    ViewSet via serializer.save(created_by=request.user).
    """
    date = serializers.CharField(max_length=50, required=False, allow_blank=True)
    year = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    event_title = serializers.CharField()

    country_lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    country_lon = serializers.DecimalField(max_digits=10, decimal_places=7)
    city_lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    city_lon = serializers.DecimalField(max_digits=10, decimal_places=7)

    agencies = serializers.ListField(
        child=serializers.CharField(max_length=150),
        required=False
    )
    presentations = PresentationCreateSerializer(many=True, required=False)

    def validate_event_title(self, value):
        if Event.objects.filter(event_title__iexact=value).exists():
            raise serializers.ValidationError(
                f"Event '{value}' already exists."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        # created_by is injected by the ViewSet, not sent by the client
        created_by = validated_data.pop('created_by', None)

        # 1. Country (get or create)
        country_name = validated_data['country']
        country = Country.objects.filter(country__iexact=country_name).first()
        if not country:
            country = Country.objects.create(
                country=country_name,
                lat=validated_data['country_lat'],
                lon=validated_data['country_lon'],
                created_by=created_by
            )
        else:
            if country.lat != validated_data['country_lat'] or country.lon != validated_data['country_lon']:
                country.lat = validated_data['country_lat']
                country.lon = validated_data['country_lon']
                country.save()

        # 2. City (get or create)
        city_name = validated_data['city']
        city = City.objects.filter(country=country, city__iexact=city_name).first()
        if not city:
            city = City.objects.create(
                country=country,
                city=city_name,
                lat=validated_data['city_lat'],
                lon=validated_data['city_lon'],
                created_by=created_by
            )
        else:
            if city.lat != validated_data['city_lat'] or city.lon != validated_data['city_lon']:
                city.lat = validated_data['city_lat']
                city.lon = validated_data['city_lon']
                city.save()

        # 3. Event
        event = Event.objects.create(
            date=validated_data.get('date', ''),
            year=validated_data.get('year'),
            type=validated_data.get('type', ''),
            country=country,
            city=city.city,
            event_title=validated_data['event_title'],
            created_by=created_by
        )

        # 4. Agencies
        for agency_name in validated_data.get('agencies', []):
            agency = Agency.objects.filter(name__iexact=agency_name).first()
            if not agency:
                agency = Agency.objects.create(name=agency_name, created_by=created_by)
            EventAgency.objects.create(event=event, agency=agency, created_by=created_by)

        # 5. Presentations & speakers
        for pres_data in validated_data.get('presentations', []):
            presentation = Presentation.objects.create(
                title=pres_data['title'],
                event=event,
                language=pres_data.get('language', []),
                url_document=pres_data.get('url', ''),
                observations=pres_data.get('observations', ''),
                created_by=created_by
            )

            for speaker_data in pres_data.get('speakers', []):
                speaker_country_name = speaker_data['country']
                speaker_country = Country.objects.filter(
                    country__iexact=speaker_country_name
                ).first()
                if not speaker_country:
                    speaker_country, _ = Country.objects.get_or_create(
                        country=speaker_country_name,
                        defaults={'lat': 0, 'lon': 0, 'created_by': created_by}
                    )

                agency_name = speaker_data.get('agency', '')
                speaker_agency = None
                if agency_name:
                    speaker_agency, _ = Agency.objects.get_or_create(
                        name=agency_name,
                        defaults={'created_by': created_by}
                    )

                speaker = Speaker.objects.filter(
                    name__iexact=speaker_data['name'],
                    country=speaker_country
                ).first()
                if not speaker:
                    speaker = Speaker.objects.create(
                        name=speaker_data['name'],
                        country=speaker_country,
                        agency=speaker_agency,
                        created_by=created_by
                    )
                else:
                    if speaker_agency and speaker.agency != speaker_agency:
                        speaker.agency = speaker_agency
                        speaker.save()

                PresentationSpeaker.objects.get_or_create(
                    presentation=presentation,
                    speaker=speaker,
                    defaults={'created_by': created_by}
                )

        return event


# ===========================================================================
# EVENT AGENCY SERIALIZERS
# ===========================================================================

class EventAgencySerializer(serializers.Serializer):
    agency_id = serializers.IntegerField(required=False, allow_null=True)
    agency_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('agency_id') and not data.get('agency_name'):
            raise serializers.ValidationError(
                "Provide 'agency_id' or 'agency_name'."
            )
        return data


class EventAgenciesUpdateSerializer(serializers.Serializer):
    agencies = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of agency IDs"
    )
    agency_names = serializers.ListField(
        child=serializers.CharField(max_length=150),
        required=False,
        help_text="List of agency names"
    )

    def validate(self, data):
        if not data.get('agencies') and not data.get('agency_names'):
            raise serializers.ValidationError(
                "Provide 'agencies' (IDs) or 'agency_names' (names)."
            )
        return data
