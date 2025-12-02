from django.contrib import admin
from FELA import models

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'long_name')
    search_fields = ('nombre', 'long_name')
admin.site.register(models.Agency, AgencyAdmin)

