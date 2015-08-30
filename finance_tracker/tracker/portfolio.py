from django.db.models import Sum

from tracker.models import Position, SecurityDataPoint


def get_position_last_value(position):
    dp = SecurityDataPoint.objects.filter(security=position.security).last()
    value = dp.unit_value * position.units
    return value


def get_security_units_for_portfolio(portfolio, security):
    agg = Position.objects.filter(portfolio=portfolio, security=security) \
                          .aggregate(total_units=Sum('units'))
    return agg['total_units']
