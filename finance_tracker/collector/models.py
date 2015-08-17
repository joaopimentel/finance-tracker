from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal
from django.utils import timezone

from lxml import html
import requests
from django.db import models

from tracker.models import Security, SecurityDataPoint


class BaseDataSource(models.Model):

    class Meta:
        abstract = True

    security = models.ForeignKey(Security)


class ExternalFileDataSource(BaseDataSource):
    """
    Gets file data from a URL. Methods to parse the file to be defined
    by subclasses.
    """
    class Meta:
        abstract = True

    file_url = models.URLField()

    def read_file(self):
        r = requests.get(self.file_url)
        return r.content

    def data_to_datapoints(self, data):
        """
        Expects a list of dicts with the keys:
            'timestamp', 'unit_value'
        """
        num_created = 0
        for d in data:
            obj, created = SecurityDataPoint.objects.update_or_create(
                security=self.security,
                timestamp=d['timestamp'],
                defaults={'unit_value': d['unit_value']},
            )
            num_created += created
        return num_created


class SpecificXMLDataSource(ExternalFileDataSource):
    """
    Expects a XML/HTML with a table like:
        <table>
            <caption></caption>
            <tr><th>DATA<th><th>PRECO<th></tr>
            <tr><td>date</td><td>price</td></tr>
            ...
    And expects that:
        - header row is Date, Price;
        - date is in dd-mm-yyyy;
        - price has a ',' for decimal point;
    """
    def iter_raw_data(self):
        content = self.read_file()
        tree = html.fromstring(content)
        for tr in tree.iter('tr'):
            vals = list(tr.iter('td'))
            if len(vals) == 0:
                # Should be the header row, skip
                continue
            yield vals[0].text_content(), vals[1].text_content()

    def convert_val(self, val_str):
        """ Converts str with decimal point ',' to Decimal """
        return Decimal(val_str.replace(',', '.'))

    def convert_date(self, date_str):
        """
        Converts a 'dd-mm-yyyy' str to a timezone-aware datetime, at 0900 UTC
        """
        naive = datetime.strptime(date_str, '%d-%m-%Y')
        naive = naive.replace(hour=9)
        return timezone.make_aware(naive, timezone=timezone.utc)

    def iter_raw_to_datapoint_data(self, iter_raw):
        for date, val in iter_raw:
            yield dict(timestamp=self.convert_date(date),
                       unit_value=self.convert_val(val))
