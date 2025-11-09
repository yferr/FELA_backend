from rest_framework import serializers
from django.db import transaction
from django.db.models import Q
from .models import (
    Country, City, Agency, Event, Presentation, 
    Speaker, PresentationSpeaker, EventAgency
)


# ============== NIVEL 1: SERIALIZERS BÁSICOS ==============

class CountrySerializer(serializers.ModelSerializer):
    """Serializer para países con coordenadas obligatorias"""
    
    class Meta:
        model = Country
        fields = ['country', 'lat', 'lon']
    
    def validate(self, data):
        """Validar que las coordenadas sean obligatorias"""
        if data.get('lat') is None or data.get('lon') is None:
            raise serializers.ValidationError({
                'coordinates': 'Las coordenadas (lat, lon) son obligatorias.'
            })
        return data
    
    def create(self, validated_data):
        """
        Get-or-create con búsqueda case-insensitive.
        Si existe, retorna el existente (mantiene capitalización original).
        Si no existe, crea nuevo.
        """
        country_name = validated_data['country']
        
        # Buscar case-insensitive
        existing = Country.objects.filter(
            country__iexact=country_name
        ).first()
        
        if existing:
            # Actualizar coordenadas si vienen diferentes
            if validated_data.get('lat') and validated_data.get('lon'):
                existing.lat = validated_data['lat']
                existing.lon = validated_data['lon']
                existing.save()
            return existing
        
        # Si no existe, crear nuevo
        return Country.objects.create(**validated_data)


class CitySerializer(serializers.ModelSerializer):
    """Serializer para ciudades con coordenadas obligatorias"""
    country = serializers.CharField()
    
    class Meta:
        model = City
        fields = ['country', 'city', 'lat', 'lon']
    
    def validate_country(self, value):
        """Validar que el país exista (case-insensitive)"""
        country = Country.objects.filter(country__iexact=value).first()
        if not country:
            raise serializers.ValidationError(
                f"El país '{value}' no existe. Créalo primero."
            )
        return value
    
    def validate(self, data):
        """Validar que las coordenadas sean obligatorias"""
        if data.get('lat') is None or data.get('lon') is None:
            raise serializers.ValidationError({
                'coordinates': 'Las coordenadas (lat, lon) son obligatorias.'
            })
        return data
    
    def create(self, validated_data):
        """
        Get-or-create con búsqueda case-insensitive.
        """
        country_name = validated_data.pop('country')
        city_name = validated_data['city']
        
        # Buscar país (case-insensitive)
        country = Country.objects.filter(country__iexact=country_name).first()
        
        # Buscar ciudad existente (case-insensitive)
        existing_city = City.objects.filter(
            country=country,
            city__iexact=city_name
        ).first()
        
        if existing_city:
            # Actualizar coordenadas si vienen diferentes
            if validated_data.get('lat') and validated_data.get('lon'):
                existing_city.lat = validated_data['lat']
                existing_city.lon = validated_data['lon']
                existing_city.save()
            return existing_city
        
        # Si no existe, crear nueva
        city = City.objects.create(
            country=country,
            city=validated_data['city'],
            lat=validated_data.get('lat'),
            lon=validated_data.get('lon')
        )
        return city


class AgencySerializer(serializers.ModelSerializer):
    """Serializer para agencias"""
    
    class Meta:
        model = Agency
        fields = ['id', 'nombre']
    
    def create(self, validated_data):
        """Get-or-create con búsqueda case-insensitive"""
        nombre = validated_data['nombre']
        
        # Buscar case-insensitive
        existing = Agency.objects.filter(nombre__iexact=nombre).first()
        if existing:
            return existing
        
        return Agency.objects.create(**validated_data)


class SpeakerSerializer(serializers.ModelSerializer):
    """Serializer para speakers (único por nombre+país)"""
    country_s = serializers.CharField()
    
    class Meta:
        model = Speaker
        fields = ['id', 'name', 'country_s', 'agency_s']
    
    def validate_country_s(self, value):
        """Validar que el país exista (case-insensitive)"""
        country = Country.objects.filter(country__iexact=value).first()
        if not country:
            raise serializers.ValidationError(
                f"El país '{value}' no existe. Créalo primero."
            )
        return value
    
    def create(self, validated_data):
        """
        Get-or-create basado en nombre + país (case-insensitive).
        Si existe, actualiza agency_s si viene diferente.
        """
        country_name = validated_data.pop('country_s')
        name = validated_data['name']
        agency_s = validated_data.get('agency_s', '')
        
        # Buscar país (case-insensitive)
        country = Country.objects.filter(country__iexact=country_name).first()
        
        # Buscar speaker existente (case-insensitive en nombre)
        existing_speaker = Speaker.objects.filter(
            name__iexact=name,
            country_s=country
        ).first()
        
        if existing_speaker:
            # Actualizar agency si viene diferente
            if agency_s and existing_speaker.agency_s != agency_s:
                existing_speaker.agency_s = agency_s
                existing_speaker.save()
            return existing_speaker
        
        # Si no existe, crear nuevo
        speaker = Speaker.objects.create(
            name=name,
            country_s=country,
            agency_s=agency_s
        )
        return speaker


class EventSerializer(serializers.ModelSerializer):
    """Serializer básico para eventos"""
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
        """Validar que país y ciudad existan y estén relacionados"""
        country_name = data.get('country_e')
        city_name = data.get('city_e')
        
        # Validar país (case-insensitive)
        country = Country.objects.filter(country__iexact=country_name).first()
        if not country:
            raise serializers.ValidationError({
                'country_e': f"El país '{country_name}' no existe."
            })
        
        # Validar ciudad (case-insensitive)
        city = City.objects.filter(
            country=country,
            city__iexact=city_name
        ).first()
        if not city:
            raise serializers.ValidationError({
                'city_e': f"La ciudad '{city_name}' no existe en '{country.country}'."
            })
        
        return data


class PresentationSerializer(serializers.ModelSerializer):
    """Serializer básico para presentaciones"""
    event_title = serializers.CharField()
    language = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    
    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'event_title', 
            'language', 'url_document', 'observations'
        ]
    
    def validate_event_title(self, value):
        """Validar que el evento exista (case-insensitive)"""
        event = Event.objects.filter(event_title__iexact=value).first()
        if not event:
            raise serializers.ValidationError(
                f"El evento '{value}' no existe. Créalo primero."
            )
        return value


# ============== NIVEL 2: SERIALIZERS DE LECTURA ANIDADOS ==============

class CountryDetailSerializer(serializers.ModelSerializer):
    cities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Country
        fields = ['country', 'lat', 'lon', 'cities_count']
    
    def get_cities_count(self, obj):
        return obj.cities.count()


class SpeakerDetailSerializer(serializers.ModelSerializer):
    country_s = serializers.CharField(source='country_s.country')
    
    class Meta:
        model = Speaker
        fields = ['id', 'name', 'country_s', 'agency_s']


class PresentationDetailSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event_title.event_title')
    event_id = serializers.IntegerField(source='event_title.id')
    event_country = serializers.CharField(source='event_title.country_e.country')
    event_city = serializers.CharField(source='event_title.city_e')
    event_year = serializers.IntegerField(source='event_title.year')
    speakers = SpeakerDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'language', 'url_document', 'observations',
            'event_id', 'event_title', 'event_country', 'event_city', 
            'event_year', 'speakers'
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    country_e = serializers.CharField(source='country_e.country')
    country_lat = serializers.DecimalField(
        source='country_e.lat', 
        max_digits=10, 
        decimal_places=7,
        read_only=True
    )
    country_lon = serializers.DecimalField(
        source='country_e.lon', 
        max_digits=10, 
        decimal_places=7,
        read_only=True
    )
    presentations = PresentationSerializer(many=True, read_only=True)
    agencies = AgencySerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'date', 'year', 'type', 
            'country_e', 'city_e', 'event_title',
            'country_lat', 'country_lon',
            'presentations', 'agencies'
        ]


# ============== NIVEL 3: SERIALIZERS DE ESCRITURA COMPLEJOS ==============

class SpeakerCreateSerializer(serializers.Serializer):
    """Serializer para crear speakers dentro de presentaciones"""
    name = serializers.CharField(max_length=200)
    country = serializers.CharField(max_length=100)
    agency = serializers.CharField(max_length=150, required=False, allow_blank=True)


class PresentationCreateSerializer(serializers.Serializer):
    """Serializer para crear presentaciones dentro de eventos"""
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
    Serializer para crear evento completo con presentaciones y speakers
    en una sola operación atómica.
    Normaliza automáticamente (case-insensitive get-or-create).
    """
    # Datos del evento
    date = serializers.CharField(max_length=50, required=False, allow_blank=True)
    year = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    event_title = serializers.CharField()
    
    # Coordenadas obligatorias
    country_lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    country_lon = serializers.DecimalField(max_digits=10, decimal_places=7)
    city_lat = serializers.DecimalField(max_digits=10, decimal_places=7)
    city_lon = serializers.DecimalField(max_digits=10, decimal_places=7)
    
    # Agencias
    agencies = serializers.ListField(
        child=serializers.CharField(max_length=150),
        required=False
    )
    
    # Presentaciones
    presentations = PresentationCreateSerializer(many=True, required=False)
    
    def validate_event_title(self, value):
        """Validar que el evento no exista (case-insensitive)"""
        if Event.objects.filter(event_title__iexact=value).exists():
            raise serializers.ValidationError(
                f"El evento '{value}' ya existe. Usa un título diferente."
            )
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        """Crea todo en una transacción atómica con normalización automática"""
        
        # 1. Obtener o crear país (case-insensitive)
        country_name = validated_data['country']
        country = Country.objects.filter(country__iexact=country_name).first()
        
        if not country:
            country = Country.objects.create(
                country=country_name,
                lat=validated_data['country_lat'],
                lon=validated_data['country_lon']
            )
        else:
            # Actualizar coordenadas si es necesario
            if country.lat != validated_data['country_lat'] or country.lon != validated_data['country_lon']:
                country.lat = validated_data['country_lat']
                country.lon = validated_data['country_lon']
                country.save()
        
        # 2. Obtener o crear ciudad (case-insensitive)
        city_name = validated_data['city']
        city = City.objects.filter(
            country=country,
            city__iexact=city_name
        ).first()
        
        if not city:
            city = City.objects.create(
                country=country,
                city=city_name,
                lat=validated_data['city_lat'],
                lon=validated_data['city_lon']
            )
        else:
            # Actualizar coordenadas si es necesario
            if city.lat != validated_data['city_lat'] or city.lon != validated_data['city_lon']:
                city.lat = validated_data['city_lat']
                city.lon = validated_data['city_lon']
                city.save()
        
        # 3. Crear evento
        event = Event.objects.create(
            date=validated_data.get('date', ''),
            year=validated_data.get('year'),
            type=validated_data.get('type', ''),
            country_e=country,
            city_e=city.city,  # Usar el nombre de la ciudad encontrada/creada
            event_title=validated_data['event_title']
        )
        
        # 4. Crear/asociar agencias (case-insensitive)
        agencies_data = validated_data.get('agencies', [])
        for agency_name in agencies_data:
            agency = Agency.objects.filter(nombre__iexact=agency_name).first()
            if not agency:
                agency = Agency.objects.create(nombre=agency_name)
            EventAgency.objects.create(id_event=event, id_agencia=agency)
        
        # 5. Crear presentaciones y speakers
        presentations_data = validated_data.get('presentations', [])
        for pres_data in presentations_data:
            presentation = Presentation.objects.create(
                title=pres_data['title'],
                event_title=event,
                language=pres_data.get('language', []),
                url_document=pres_data.get('url', ''),
                observations=pres_data.get('observations', '')
            )
            
            # 6. Crear/asociar speakers (case-insensitive por nombre+país)
            speakers_data = pres_data.get('speakers', [])
            for speaker_data in speakers_data:
                speaker_country_name = speaker_data['country']
                speaker_name = speaker_data['name']
                speaker_agency = speaker_data.get('agency', '')
                
                # Buscar/crear país del speaker
                speaker_country = Country.objects.filter(
                    country__iexact=speaker_country_name
                ).first()
                
                if not speaker_country:
                    # Si el país no existe, usar "-" como país desconocido
                    speaker_country = Country.objects.filter(country="-").first()
                    if not speaker_country:
                        speaker_country = Country.objects.create(
                            country="-",
                            lat=0,
                            lon=0
                        )
                
                # Buscar/crear speaker (case-insensitive por nombre+país)
                speaker = Speaker.objects.filter(
                    name__iexact=speaker_name,
                    country_s=speaker_country
                ).first()
                
                if not speaker:
                    speaker = Speaker.objects.create(
                        name=speaker_name,
                        country_s=speaker_country,
                        agency_s=speaker_agency
                    )
                else:
                    # Actualizar agencia si viene diferente
                    if speaker_agency and speaker.agency_s != speaker_agency:
                        speaker.agency_s = speaker_agency
                        speaker.save()
                
                # Asociar speaker con presentación
                PresentationSpeaker.objects.get_or_create(
                    id_presentation=presentation,
                    id_speaker=speaker
                )
        
        return event