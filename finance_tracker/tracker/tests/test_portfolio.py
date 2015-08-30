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
    get_total_value_on_security,
    get_security_units_for_portfolio,
)


class PortfolioTest(TestCase):

    def setUp(self):
        self.sec = Security.objects.create(name='sec', isin='sec')
        self.portfolio = Portfolio.objects.create(name='portfolio')

        timestamps = [
            datetime(2014, 10, 24, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 29, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 30, 9, 0, 0, tzinfo=timezone.utc),
        ]
        vals = [
            Decimal('1.0'),
            Decimal('1.5'),
            Decimal('2.0'),
            Decimal('2.5'),
            Decimal('3.0'),
        ]
        for t, v in zip(timestamps, vals):
            SecurityDataPoint.objects.create(security=self.sec,
                                             timestamp=t,
                                             unit_value=v)
        self.pos_timestamps = [
            datetime(2014, 10, 24, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 29, 9, 0, 0, tzinfo=timezone.utc),
        ]

    def test_position_value(self):
        pos = Position(
            security=self.sec,
            timestamp=datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            units=Decimal('1.0'),
            portfolio=self.portfolio,
        )
        val = get_position_last_value(pos)
        self.assertEqual(val, Decimal('3.0'))
        # Change number of units for position
        pos.units = Decimal('3.0')
        val = get_position_last_value(pos)
        self.assertEqual(val, Decimal('9.0'))

    def test_total_units(self):
        position_units = [
            Decimal('1.0'),
            Decimal('3.0'),
            Decimal('-1.5'),
            Decimal('-2.0'),
        ]
        [Position.objects.create(security=self.sec,
                                 timestamp=t,
                                 units=u,
                                 portfolio=self.portfolio)
            for u, t in zip(position_units, self.pos_timestamps)]
        total_units = get_security_units_for_portfolio(
            self.portfolio, self.sec)
        self.assertEqual(total_units, Decimal('0.5'))
        #)Test `until` param (until is exclusive)
        total_units = get_security_units_for_portfolio(
            self.portfolio, self.sec,
            until=datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(total_units, Decimal('4.0'))
        total_units = get_security_units_for_portfolio(
            self.portfolio, self.sec,
            until=datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(total_units, Decimal('2.5'))

    def test_total_value_on_security(self):
        position_units = [
            Decimal('1.0'),
            Decimal('3.0'),
            Decimal('-1.5'),
            Decimal('-2.0'),
        ]
        [Position.objects.create(security=self.sec,
                                 timestamp=t,
                                 units=u,
                                 portfolio=self.portfolio)
            for u, t in zip(position_units, self.pos_timestamps)]
        # On 2014-10-29: 0.5 * 2.5
        total_value = get_total_value_on_security(
            self.portfolio,
            self.sec,
            datetime(2014, 10, 29, 9, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(total_value, Decimal('1.25'))
        # On 2014-10-28: 2.5 * 2.0
        total_value = get_total_value_on_security(
            self.portfolio,
            self.sec,
            datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(total_value, Decimal('5.0'))
