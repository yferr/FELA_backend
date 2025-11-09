from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CountryViewSet,
    CityViewSet,
    AgencyViewSet,
    EventViewSet,
    PresentationViewSet,
    SpeakerViewSet,
    PresentationSpeakerViewSet
)

# Router para registrar los ViewSets
router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'agencies', AgencyViewSet, basename='agency')
router.register(r'events', EventViewSet, basename='event')
router.register(r'presentations', PresentationViewSet, basename='presentation')
router.register(r'speakers', SpeakerViewSet, basename='speaker')
router.register(r'presentation-speakers', PresentationSpeakerViewSet, basename='presentation-speaker')

urlpatterns = [
    path('', include(router.urls)),
]