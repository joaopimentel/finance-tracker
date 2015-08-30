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
from tracker.portfolio import get_position_last_value


class PositionTest(TestCase):

    def setUp(self):
        self.sec = Security.objects.create(name='sec', isin='sec')
        portfolio = Portfolio.objects.create(name='portfolio')

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
        self.pos = Position(
            security=self.sec,
            timestamp=datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            units=Decimal('1.0'),
            portfolio=portfolio,
        )

    def test_position_value(self):
        val = get_position_last_value(self.pos)
        self.assertEqual(val, Decimal('2.0'))
        # Change number of units for position
        self.pos.units = Decimal('3.0')
        val = get_position_last_value(self.pos)
        self.assertEqual(val, Decimal('6.0'))
