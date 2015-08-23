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
    currency = models.CharField(max_length=3, default='EUR')
    detail_url = models.URLField(null=True, blank=True)

    def __str__(self):  # pragma: no cover
        return '%s (%s)' % (self.name, self.isin)

    def get_datapoint_at_time(self, timestamp):
        """
        Gets the first SecurityDataPoint for this security that has the
        timestamp greater or equal to ``timestamp``.
        """
        return SecurityDataPoint.objects.filter(security=self,
                                                timestamp__gte=timestamp) \
                                        .first()


@python_2_unicode_compatible
class SecurityDataPoint(models.Model):

    security = models.ForeignKey(Security)
    timestamp = models.DateTimeField()
    unit_value = models.DecimalField(max_digits=7, decimal_places=4)

    class Meta:
        index_together = ['security', 'timestamp']

    def __str__(self):  # pragma: no cover
        return '%s in %s: %s %s' % (
            self.security.name,
            self.timestamp,
            self.unit_value,
            self.security.currency,
        )


@python_2_unicode_compatible
class Portfolio(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):  # pragma: no cover
        return '%s' % self.name


@python_2_unicode_compatible
class Position(models.Model):

    security = models.ForeignKey(Security)
    timestamp = models.DateTimeField()
    units = models.DecimalField(max_digits=7, decimal_places=4)
    portfolio = models.ForeignKey(Portfolio)

    class Meta:
        index_together = ['portfolio', 'timestamp']
        ordering = ['timestamp']

    def __str__(self):  # pragma: no cover
        return '%s - %s in %s (%s units)' % (
            self.portfolio,
            self.security.name,
            self.timestamp,
            self.units,
        )
