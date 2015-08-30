from django.db.models import Sum

from tracker.models import Position, SecurityDataPoint


def get_position_last_value(position):
    dp = SecurityDataPoint.objects.filter(security=position.security).last()
    value = dp.unit_value * position.units
    return value


def get_security_units_for_portfolio(portfolio, security, until=None):
    """
    Sums the amount of units for a security, until some date (timestamp<=until)
    """
    qs = Position.objects.filter(portfolio=portfolio, security=security)
    if until is not None:
        qs = qs.filter(timestamp__lte=until)
    agg = qs.aggregate(total_units=Sum('units'))
    return agg['total_units']
