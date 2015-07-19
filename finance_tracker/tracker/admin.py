from django.contrib import admin

from .models import Security, SecurityDataPoint


admin.site.register(Security)
admin.site.register(SecurityDataPoint)
