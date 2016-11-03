# About Pymetrics

A simple library to publis metrics to InfluxDB periodically.

Includes some extras, as a a wsgi middleware.

[![CircleCI](https://circleci.com/gh/cliixtech/pymetric/tree/master.svg?style=svg)](https://circleci.com/gh/cliixtech/pymetric/tree/master)

# Installing dependencies

First of all, create a virtualenv using Python 3.5. After creating the virtualenv
run ```pip install -r dev_requirements.txt```.

# Testing

To run local tests use:

``
nosetests-3.4 tests/
``


# Usage

``
from pymetric.metrics import MetricRegistry, metric as m 

registry = MetricsRegistry(influx_client,
                           300,  # interval in seconds
                           {'environment': 'prod'}  # Some extra tags for all metrics
                           )
registry.add_metric(m('name', 100, {'key': 'value'}))
``