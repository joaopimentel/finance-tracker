from django.contrib import admin

from .models import SpecificXMLDataSource


class SpecificXMLDataSourceAdmin(admin.ModelAdmin):
    list_display = ('security', 'file_url')

admin.site.register(SpecificXMLDataSource, SpecificXMLDataSourceAdmin)
