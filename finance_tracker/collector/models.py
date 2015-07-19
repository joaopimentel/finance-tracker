from __future__ import unicode_literals

from django.db import models

from tracker.models import Security


class BaseDataSource(models.Model):

    class Meta:
        abstract = True

    security = models.ForeignKey(Security)


class ExternalCSVDataSource(BaseDataSource):
    """
    Gets CSV data from a URL. Methods to parse the CSV to be defined
    by subclasses.
    """
    csv_url = models.URLField()

    def csv_to_datapoints(self):
        raise NotImplementedError
