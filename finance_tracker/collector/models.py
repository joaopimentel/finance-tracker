from __future__ import unicode_literals

from lxml import html
import requests
from django.db import models

from tracker.models import Security


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

    def data_to_datapoints(self):
        raise NotImplementedError


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



