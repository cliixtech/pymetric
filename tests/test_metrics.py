from unittest import TestCase
from unittest.mock import create_autospec

from influxdb.client import InfluxDBClient
from nose.tools import istest

from pymetric.metrics import metric, MetricsRegistry
import time


class MetricsTest(TestCase):
    @istest
    def create_metric(self):
        m = metric('testing', 5, {'key': 'value'})
        self.assertEqual('testing', m.name)
        self.assertEqual({"value": 5}, m.values)
        self.assertEqual({'key': 'value'}, m.tags)

    @istest
    def metric_extra_tags(self):
        m = metric('testing', 5, {'key': 'value'})
        m.extra_tags({'other': 'some'})
        self.assertEqual({'key': 'value',
                          'other': 'some'}, m.tags)

    @istest
    def metric_as_dict(self):
        m = metric('testing', 5, {'key': 'value'})
        expected = {"measurement": 'testing',
                    "tags": {'key': 'value'},
                    'fields': {'value': 5},
                    'time': m.time}
        self.assertEqual(expected, m.as_dict())

    @istest
    def publish_metrics_periodicaly(self):
        m_publisher = create_autospec(InfluxDBClient)
        m1 = metric('testing', 5, {'key': 'value'})
        m2 = metric('testing', 1, {'key': 'other'})
        m3 = metric('testing', 2, {'key': 'some'})

        registry = MetricsRegistry(m_publisher, 0.5, {'testing': True})

        registry.add_metric(m1)
        registry.start()
        registry.add_metrics([m2, m3])

        time.sleep(0.7)

        expected = [m for m in
                    map(lambda x: x.extra_tags({'testing': True}).as_dict(),
                        [m1, m2, m3])]
        m_publisher.write_points.assert_called_once_with(expected)
