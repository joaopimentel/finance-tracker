from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from tracker.models import Security, SecurityDataPoint


class SecurityTest(TestCase):

    def setUp(self):
        self.sec1 = Security.objects.create(name='sec1', isin='sec1')
        self.sec2 = Security.objects.create(name='sec2', isin='sec2')

        timestamps = [
            datetime(2014, 10, 23, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 24, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 27, 9, 0, 0, tzinfo=timezone.utc),
            datetime(2014, 10, 28, 9, 0, 0, tzinfo=timezone.utc),
        ]
        sec1_vals = [
            Decimal('1.0'),
            Decimal('1.5'),
            Decimal('2.0'),
            Decimal('2.5'),
        ]
        sec2_vals = [
            Decimal('3.0'),
            Decimal('4.0'),
            Decimal('5.0'),
            Decimal('6.0'),
        ]
        for t, v in zip(timestamps, sec1_vals):
            SecurityDataPoint.objects.create(security=self.sec1,
                                             timestamp=t,
                                             unit_value=v)
        for t, v in zip(timestamps, sec2_vals):
            SecurityDataPoint.objects.create(security=self.sec2,
                                             timestamp=t,
                                             unit_value=v)

    def test_datapoint_at_time(self):
        dp = self.sec1.get_datapoint_at_time(
            datetime(2014, 10, 24, 9, 0, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(dp.unit_value, Decimal('1.5'))
        dp = self.sec1.get_datapoint_at_time(
            datetime(2014, 10, 25, 9, 0, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(dp.unit_value, Decimal('2.0'))
        dp = self.sec2.get_datapoint_at_time(
            datetime(2014, 10, 25, 9, 0, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(dp.unit_value, Decimal('5.0'))
