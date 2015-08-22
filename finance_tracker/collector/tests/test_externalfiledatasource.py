from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from collector.models import ExternalFileDataSource
from tracker.models import Security, SecurityDataPoint


class ExternalFileDataSourceTest(TestCase):

    def setUp(self):
        self.security = Security.objects.create(name='zed', isin='zed')
        self.source = ExternalFileDataSource(
            security=self.security,
            file_url='http://example.com')

    def test_data_to_datapoints(self):

        timestamp1 = datetime(2014, 10, 29, 9, 0, 0, tzinfo=timezone.utc)
        timestamp2 = datetime(2014, 10, 30, 9, 0, 0, tzinfo=timezone.utc)
        timestamp3 = datetime(2014, 10, 31, 9, 0, 0, tzinfo=timezone.utc)
        data = [
            {'timestamp': timestamp1, 'unit_value': Decimal('1.0')},
            {'timestamp': timestamp2, 'unit_value': Decimal('2.0')},
            {'timestamp': timestamp3, 'unit_value': Decimal('3.0')},
        ]
        n = self.source.data_to_datapoints(data)
        self.assertEqual(n, 3)
