from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from tracker.models import (
    Security,
    SecurityDataPoint,
    Portfolio,
    Position,
)
from tracker.portfolio import (
    get_position_last_value,
    get_security_units_for_portfolio,
)


class PositionTest(TestCase):

    def setUp(self):
        self.sec = Security.objects.create(name='sec', isin='sec')
        self.portfolio = Portfolio.objects.create(name='portfolio')

        timestamps = [
            datetime(2014, 10, 24, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc),
        ]
        vals = [
            Decimal('1.0'),
            Decimal('1.5'),
            Decimal('2.0'),
        ]
        for t, v in zip(timestamps, vals):
            SecurityDataPoint.objects.create(security=self.sec,
                                             timestamp=t,
                                             unit_value=v)

    def test_position_value(self):
        pos = Position(
            security=self.sec,
            timestamp=datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            units=Decimal('1.0'),
            portfolio=self.portfolio,
        )
        val = get_position_last_value(pos)
        self.assertEqual(val, Decimal('2.0'))
        # Change number of units for position
        pos.units = Decimal('3.0')
        val = get_position_last_value(pos)
        self.assertEqual(val, Decimal('6.0'))

    def test_total_units(self):
        position_units = [
            Decimal('1.0'),
            Decimal('3.0'),
            Decimal('-1.5'),
            Decimal('-2.0'),
        ]
        timestamps = [
            datetime(2014, 10, 24, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 29, 9, 0, 0, tzinfo=timezone.utc),
        ]
        [Position.objects.create(security=self.sec,
                                 timestamp=t,
                                 units=u,
                                 portfolio=self.portfolio)
            for u, t in zip(position_units, timestamps)]
        total_units = get_security_units_for_portfolio(
            self.portfolio, self.sec)
        self.assertEqual(total_units, Decimal('0.5'))
        # Test `until` param
        total_units = get_security_units_for_portfolio(
            self.portfolio, self.sec,
            until=datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(total_units, Decimal('4.0'))
        total_units = get_security_units_for_portfolio(
            self.portfolio, self.sec,
            until=datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(total_units, Decimal('2.5'))
