from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Security(models.Model):
    """
    Mutual fund, ETF, bond, stock, warrant...
    """

    name = models.CharField(max_length=127)
    isin = models.CharField(max_length=12)
    detail_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.isin)


@python_2_unicode_compatible
class SecurityDataPoint(models.Model):

    security = models.ForeignKey(Security)
    timestamp = models.DateTimeField()
    currency = models.CharField(max_length=3, default='EUR')
    unit_value = models.DecimalField(max_digits=7, decimal_places=4)

    class Meta:
        index_together = ['security', 'timestamp']

    def __str__(self):
        return '%s in %s: %s %s' % (
            self.security.name,
            self.timestamp,
            self.unit_value,
            self.currency,
        )
