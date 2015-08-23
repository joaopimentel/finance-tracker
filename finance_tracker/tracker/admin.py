from django.contrib import admin

from .models import (
    Portfolio,
    Position,
    Security,
    SecurityDataPoint,
)


class SecurityDataPointAdmin(admin.ModelAdmin):
    def time_format(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d (%H:%M:%S)")
    time_format.admin_order_field = 'timestamp'
    time_format.short_description = 'Timestamp'

    list_display = ('time_format', 'security', 'unit_value')


admin.site.register(Security)
admin.site.register(SecurityDataPoint, SecurityDataPointAdmin)

admin.site.register(Portfolio)


class PositionAdmin(admin.ModelAdmin):
    def time_format(self, obj):
        return obj.timestamp.strftime("%Y-%m-%d (%H:%M:%S)")
    time_format.admin_order_field = 'timestamp'
    time_format.short_description = 'Timestamp'

    list_display = ('portfolio', 'time_format', 'security', 'units')


admin.site.register(Position, PositionAdmin)
