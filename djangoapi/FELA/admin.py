from django.contrib import admin
from FELA import models

# class AgencyAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'long_name')
#     search_fields = ('name', 'long_name')
# admin.site.register(models.Agency, AgencyAdmin)

# class CountryAdmin(admin.ModelAdmin):
#     list_display = ('country', 'lat', 'lon')
#     search_fields = ('country',)
# admin.site.register(models.Country, CountryAdmin)

# class CityAdmin(admin.ModelAdmin):
#     list_display = ('city', 'lat', 'lon')
#     search_fields = ('city',)
# admin.site.register(models.City, CityAdmin)

# class EventAdmin(admin.ModelAdmin):
#     list_display = ('id', 'date', 'year', 'type', 'country_e', 'city_e', 'event_title')
#     search_fields = ('date', 'year', 'type', 'country_e', 'city_e', 'event_title')
# admin.site.register(models.Event, EventAdmin)

# class PresentationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'event_title', 'language', 'url_document', 'observations')
#     search_fields = ('title', 'event_title', 'language')
# admin.site.register(models.Presentation, PresentationAdmin)

# class SpeakerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'country_s','agency_s')
#     search_fields = ('name', 'country_s','agency_s')
# admin.site.register(models.Speaker, SpeakerAdmin)

# class PresentationSpeakerAdmin(admin.ModelAdmin):
#     list_display = ('presentation', 'speaker')
#     search_fields = ('presentation', 'speaker')
# admin.site.register(models.PresentationSpeaker, PresentationSpeakerAdmin)

# class EventAgencyAdmin(admin.ModelAdmin):
#     list_display = ('event', 'agency')
#     search_fields = ('event', 'agency')
# admin.site.register(models.EventAgency, EventAgencyAdmin)

