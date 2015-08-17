
from mock import patch

from django.test import TestCase

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
class SpecificXLMDataSourceTest(TestCase):

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