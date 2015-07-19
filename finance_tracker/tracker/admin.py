from django.contrib import admin

from .models import Security, SecurityDataPoint


class SecurityDataPointAdmin(admin.ModelAdmin):
    def time_format(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d (%H:%M:%S)")
    time_format.admin_order_field = 'timestamp'
    time_format.short_description = 'Timestamp'

    list_display = ('time_format', 'security', 'unit_value', 'currency')


admin.site.register(Security)
admin.site.register(SecurityDataPoint, SecurityDataPointAdmin)
