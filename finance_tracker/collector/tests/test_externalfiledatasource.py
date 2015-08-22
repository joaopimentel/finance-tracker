from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
import responses

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
        sec_dps = SecurityDataPoint.objects.filter(security=self.security) \
                                           .order_by('timestamp')
        for dp, expected in zip(sec_dps, data):
            self.assertEqual(dp.timestamp, expected['timestamp'])
            self.assertEqual(dp.unit_value, expected['unit_value'])

    @responses.activate
    def test_read_file(self):
        responses.add(responses.GET, self.source.file_url,
                      body=b'somecontent',
                      content_type='application/octet-stream')
        content = self.source.read_file()
        self.assertEqual(content, 'somecontent')
