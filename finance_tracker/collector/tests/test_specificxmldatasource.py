from datetime import datetime
from decimal import Decimal

from mock import patch

from django.test import TestCase
from django.utils import timezone

from tracker.models import Security
from collector.models import SpecificXMLDataSource


SAMPLE_XML_CONTENT = '''
<div>
    <table cellspacing="0" rules="all" border="1">
        <caption>SKIP</caption>
        <tr><th scope="col">DATA</th><th scope="col">PRECO</th></tr>
        <tr><td>29-10-2014</td><td>130,29</td></tr>
        <tr><td>30-10-2014</td><td>129,70</td></tr>
        <tr><td>31-10-2014</td><td>133,53</td></tr>
    </table>
</div>
'''


@patch('collector.models.SpecificXMLDataSource.read_file',
       new=lambda x: SAMPLE_XML_CONTENT)
class SpecificXMLDataSourceTest(TestCase):

    def setUp(self):
        self.security = Security.objects.create(name='zed', isin='zed')
        self.datasource = SpecificXMLDataSource.objects.create(
            security=self.security,
            file_url='http://example.com')

    def test_raw_data(self):
        expected_raw_data = (
            ('29-10-2014', '130,29'),
            ('30-10-2014', '129,70'),
            ('31-10-2014', '133,53'),
        )
        for expected, got in zip(self.datasource.iter_raw_data(),
                                 expected_raw_data):
            self.assertEqual(expected, got)

    def test_convert_val(self):
        conv = self.datasource.convert_val
        self.assertEqual(conv('123,45'), Decimal('123.45'))
        self.assertEqual(conv('123'), Decimal('123.0'))
        self.assertEqual(conv('0,123'), Decimal('0.123'))

    def test_convert_date(self):
        expected = datetime(2014, 10, 29, 9, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(self.datasource.convert_date('29-10-2014'),
                         expected)

    def test_iter_raw_to_datapoint_data(self):
        raw = (
            ('29-10-2014', '130,29'),
            ('30-10-2014', '129,70'),
            ('31-10-2014', '133,53'),
        )
        datapoint_data = self.datasource.iter_raw_to_datapoint_data(raw)
        expected = [
            dict(timestamp=datetime(2014, 10, 29, 9, 0, 0,
                                    tzinfo=timezone.utc),
                 unit_value=Decimal('130.29')),
            dict(timestamp=datetime(2014, 10, 30, 9, 0, 0,
                                    tzinfo=timezone.utc),
                 unit_value=Decimal('129.70')),
            dict(timestamp=datetime(2014, 10, 31, 9, 0, 0,
                                    tzinfo=timezone.utc),
                 unit_value=Decimal('133.53')),
        ]
        for val, expected in zip(datapoint_data, expected):
            self.assertEqual(val, expected)
