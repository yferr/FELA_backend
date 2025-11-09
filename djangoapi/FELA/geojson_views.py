from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from .geojson_builder import GeoJSONBuilder


GEOJSON_CACHE_KEY = 'geojson_complete'
CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 días en segundos


@api_view(['GET'])
@permission_classes([AllowAny])
def geojson_complete_view(request):
    """
    Endpoint que retorna el GeoJSON completo con todos los eventos,
    presentaciones, speakers y coordenadas.
    
    GET /api/geojson/
    
    Respuesta:
    {
        "metadata": {
            "generated_at": "2025-11-04T10:30:00",
            "total_events": 24,
            "years": [2017, 2018, 2019, ...],
            "cached": true
        },
        "events": {
            "2017": {
                "Event Title": [{ event_data }]
            }
        },
        "citiesGeoJSON": {
            "type": "FeatureCollection",
            "features": [...]
        },
        "countriesGeoJSON": {
            "type": "FeatureCollection",
            "features": [...]
        }
    }
    """
    
    # Intentar obtener desde caché
    geojson_data = cache.get(GEOJSON_CACHE_KEY)
    
    if geojson_data is not None:
        # Actualizar metadata para indicar que viene de caché
        geojson_data['metadata']['cached'] = True
        return Response(geojson_data)
    
    # Si no está en caché, generar
    builder = GeoJSONBuilder()
    geojson_data = builder.build_complete_geojson()
    
    # Guardar en caché
    cache.set(GEOJSON_CACHE_KEY, geojson_data, CACHE_TIMEOUT)
    
    # Indicar que es nuevo (no del caché)
    geojson_data['metadata']['cached'] = False
    
    return Response(geojson_data)


@api_view(['POST'])
@permission_classes([AllowAny])  # Cambiar a IsAdminUser si prefieres
def geojson_refresh_view(request):
    """
    Endpoint manual para invalidar el caché del GeoJSON.
    Útil para forzar regeneración sin esperar signals.
    
    POST /api/geojson/refresh/
    
    Respuesta:
    {
        "message": "Cache invalidado exitosamente. El próximo request generará un nuevo GeoJSON.",
        "cache_key": "geojson_complete"
    }
    """
    cache.delete(GEOJSON_CACHE_KEY)
    
    return Response({
        "message": "Cache invalidado exitosamente. El próximo request generará un nuevo GeoJSON.",
        "cache_key": GEOJSON_CACHE_KEY
    })