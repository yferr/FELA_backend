from rest_framework import serializers
from django.db import transaction
from core.myLib.geoModelSerializer import GeoModelSerializer
from .models import (
    Country, City, Agency, Event, Presentation, 
    Speaker, PresentationSpeaker, EventAgency
)


# ============== NIVEL 1: SERIALIZERS BÁSICOS ==============

class CountrySerializer(serializers.ModelSerializer):
    geoms_as_wkt = True

    class Meta:
        model = Country
        fields = GeoModelSerializer.Meta.fields + ['country', 'geom']
        
    def validate_geom(self, value):
        """Validates if a geometry is valid.
            Do not do anythin special. Simple is an example of how to override the father method
        """
        print('validate_geom, child')
        return super().validate_geom(value)


class CitySerializer(serializers.ModelSerializer):
    geoms_as_wkt = True
    country = serializers.CharField()

    class Meta:
        model = City
        fields = GeoModelSerializer.Meta.fields + ['country', 'city', 'geom']

    def validate_geom(self, value):
        """Validates if a geometry is valid.
            Do not do anythin special. Simple is an example of how to override the father method
        """
        print('validate_geom, child')
        return super().validate_geom(value)

    def validate_country(self, value):
        """Valida que el país exista"""
        if not Country.objects.filter(country=value).exists():
            raise serializers.ValidationError(
                f"El país '{value}' no existe. Créalo primero o verifica el nombre."
            )
        return value

    def create(self, validated_data):
        """Obtiene o crea la ciudad"""
        country_name = validated_data.pop('country')
        country = Country.objects.get(country=country_name)
        city, created = City.objects.get_or_create(
            country=country,
            city=validated_data['city'],
            defaults={'geom': validated_data.get('geom')}
        )
        return city


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', 'nombre']

    def create(self, validated_data):
        """Obtiene o crea la agencia"""
        agency, created = Agency.objects.get_or_create(
            nombre=validated_data['nombre']
        )
        return agency


class EventSerializer(serializers.ModelSerializer):
    country_e = serializers.CharField()
    agencies = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Agency.objects.all(),
        required=False
    )

    class Meta:
        model = Event
        fields = [
            'id', 'date', 'year', 'type', 
            'country_e', 'city_e', 'event_title', 'agencies'
        ]

    def validate(self, data):
        """Valida que país y ciudad existan y estén relacionados"""
        country_name = data.get('country_e')
        city_name = data.get('city_e')

        # Validar país
        if not Country.objects.filter(country=country_name).exists():
            raise serializers.ValidationError({
                'country_e': f"El país '{country_name}' no existe."
            })

        # Validar ciudad
        if not City.objects.filter(country__country=country_name, city=city_name).exists():
            raise serializers.ValidationError({
                'city_e': f"La ciudad '{city_name}' no existe en '{country_name}'."
            })

        return data


class PresentationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField()

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'event_title', 
            'language', 'url_document', 'observations'
        ]

    def validate_event_title(self, value):
        """Valida que el evento exista"""
        if not Event.objects.filter(event_title=value).exists():
            raise serializers.ValidationError(
                f"El evento '{value}' no existe. Créalo primero."
            )
        return value


class SpeakerSerializer(serializers.ModelSerializer):
    country_s = serializers.CharField()

    class Meta:
        model = Speaker
        fields = ['id', 'name', 'country_s', 'agency_s']

    def validate_country_s(self, value):
        """Valida que el país exista"""
        if not Country.objects.filter(country=value).exists():
            raise serializers.ValidationError(
                f"El país '{value}' no existe. Créalo primero."
            )
        return value

    def create(self, validated_data):
        """Obtiene o crea el speaker"""
        country_name = validated_data.pop('country_s')
        country = Country.objects.get(country=country_name)
        speaker, created = Speaker.objects.get_or_create(
            name=validated_data['name'],
            defaults={
                'country_s': country,
                'agency_s': validated_data.get('agency_s')
            }
        )
        return speaker


# ============== NIVEL 2: SERIALIZERS DE LECTURA ANIDADOS ==============

class CountryDetailSerializer(serializers.ModelSerializer):
    geom_wkt = serializers.SerializerMethodField()
    cities_count = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['country', 'geom', 'geom_wkt', 'cities_count']

    def get_geom_wkt(self, obj):
        return obj.geom.wkt if obj.geom else None

    def get_cities_count(self, obj):
        return obj.cities.count()


class SpeakerDetailSerializer(serializers.ModelSerializer):
    country_s = serializers.CharField(source='country_s.country')
    country_geom = serializers.SerializerMethodField()

    class Meta:
        model = Speaker
        fields = ['id', 'name', 'country_s', 'country_geom', 'agency_s']

    def get_country_geom(self, obj):
        return obj.country_s.geom.wkt if obj.country_s.geom else None


class PresentationDetailSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event_title.event_title')
    event_id = serializers.IntegerField(source='event_title.id')
    event_country = serializers.CharField(source='event_title.country_e.country')
    event_city = serializers.CharField(source='event_title.city_e')
    event_year = serializers.IntegerField(source='event_title.year')
    country_geom = serializers.SerializerMethodField()
    city_geom = serializers.SerializerMethodField()
    speakers = SpeakerDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'language', 'url_document', 'observations',
            'event_id', 'event_title', 'event_country', 'event_city', 
            'event_year', 'country_geom', 'city_geom', 'speakers'
        ]

    def get_country_geom(self, obj):
        country = obj.event_title.country_e
        return country.geom.wkt if country.geom else None

    def get_city_geom(self, obj):
        city = obj.event_title.city_object
        return city.geom.wkt if city and city.geom else None


class EventDetailSerializer(serializers.ModelSerializer):
    country_e = serializers.CharField(source='country_e.country')
    country_geom = serializers.SerializerMethodField()
    city_geom = serializers.SerializerMethodField()
    presentations = PresentationSerializer(many=True, read_only=True)
    agencies = AgencySerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'date', 'year', 'type', 
            'country_e', 'city_e', 'event_title',
            'country_geom', 'city_geom',
            'presentations', 'agencies'
        ]

    def get_country_geom(self, obj):
        return obj.country_e.geom.wkt if obj.country_e.geom else None

    def get_city_geom(self, obj):
        city = obj.city_object
        return city.geom.wkt if city and city.geom else None


# ============== NIVEL 3: SERIALIZERS DE ESCRITURA COMPLEJOS ==============

class SpeakerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=100)
    agency = serializers.CharField(max_length=150, required=False, allow_blank=True)


class PresentationCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    language = serializers.CharField(max_length=50, required=False, allow_blank=True)
    url = serializers.CharField(required=False, allow_blank=True)
    observations = serializers.CharField(required=False, allow_blank=True)
    speakers = SpeakerCreateSerializer(many=True, required=False)


class EventCompleteCreateSerializer(serializers.Serializer):
    """
    Serializer para crear evento completo con presentaciones y speakers
    en una sola operación atómica.
    """
    # Datos del evento
    date = serializers.CharField(max_length=50, required=False, allow_blank=True)
    year = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    event_title = serializers.CharField()
    
    # Coordenadas opcionales
    country_lat = serializers.FloatField(required=False, allow_null=True)
    country_lon = serializers.FloatField(required=False, allow_null=True)
    city_lat = serializers.FloatField(required=False, allow_null=True)
    city_lon = serializers.FloatField(required=False, allow_null=True)
    
    # Agencias
    agencies = serializers.ListField(
        child=serializers.CharField(max_length=150),
        required=False
    )
    
    # Presentaciones
    presentations = PresentationCreateSerializer(many=True, required=False)

    def validate_event_title(self, value):
        """Valida que el evento no exista"""
        if Event.objects.filter(event_title=value).exists():
            raise serializers.ValidationError(
                f"El evento '{value}' ya existe. Usa un título diferente."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        """Crea todo en una transacción atómica"""
        from django.contrib.gis.geos import Point
        
        # 1. Obtener o crear país
        country_name = validated_data['country']
        country_geom = None
        if validated_data.get('country_lat') and validated_data.get('country_lon'):
            country_geom = Point(
                validated_data['country_lon'], 
                validated_data['country_lat'],
                srid=4326
            )
        
        country, _ = Country.objects.get_or_create(
            country=country_name,
            defaults={'geom': country_geom}
        )

        # 2. Obtener o crear ciudad
        city_name = validated_data['city']
        city_geom = None
        if validated_data.get('city_lat') and validated_data.get('city_lon'):
            city_geom = Point(
                validated_data['city_lon'],
                validated_data['city_lat'],
                srid=4326
            )
        
        city, _ = City.objects.get_or_create(
            country=country,
            city=city_name,
            defaults={'geom': city_geom}
        )

        # 3. Crear evento
        event = Event.objects.create(
            date=validated_data.get('date', ''),
            year=validated_data.get('year'),
            type=validated_data.get('type', ''),
            country_e=country,
            city_e=city_name,
            event_title=validated_data['event_title']
        )

        # 4. Crear/asociar agencias
        agencies_data = validated_data.get('agencies', [])
        for agency_name in agencies_data:
            agency, _ = Agency.objects.get_or_create(nombre=agency_name)
            EventAgency.objects.create(id_event=event, id_agencia=agency)

        # 5. Crear presentaciones y speakers
        presentations_data = validated_data.get('presentations', [])
        for pres_data in presentations_data:
            presentation = Presentation.objects.create(
                title=pres_data['title'],
                event_title=event,
                language=pres_data.get('language', ''),
                url_document=pres_data.get('url', ''),
                observations=pres_data.get('observations', '')
            )

            # 6. Crear/asociar speakers
            speakers_data = pres_data.get('speakers', [])
            for speaker_data in speakers_data:
                speaker_country_name = speaker_data['country']
                speaker_country, _ = Country.objects.get_or_create(
                    country=speaker_country_name
                )
                
                speaker, _ = Speaker.objects.get_or_create(
                    name=speaker_data['name'],
                    defaults={
                        'country_s': speaker_country,
                        'agency_s': speaker_data.get('agency', '')
                    }
                )
                
                PresentationSpeaker.objects.create(
                    id_presentation=presentation,
                    id_speaker=speaker
                )

        return event