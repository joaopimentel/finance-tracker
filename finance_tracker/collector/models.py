from __future__ import unicode_literals

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
    file_url = models.URLField()

    def read_file(self):
        r = requests.get(self.file_url)
        return r.content

    def data_to_datapoints(self):
        raise NotImplementedError
