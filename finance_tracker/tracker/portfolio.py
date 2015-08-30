from tracker.models import SecurityDataPoint


def get_position_last_value(position):
    dp = SecurityDataPoint.objects.filter(security=position.security).last()
    value = dp.unit_value * position.units
    return value
