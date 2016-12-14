from datetime import datetime
from threading import Thread, RLock
import logging
import time

log = logging.getLogger(__name__)


class _Metric:
    def __init__(self, name, values, tags):
        self._name = name
        self._values = values
        self._tags = tags
        self._time = ("%sZ" %
                      datetime.utcnow().replace(microsecond=0).isoformat())

    @property
    def name(self):
        return self._name

    @property
    def values(self):
        return self._values

    @property
    def tags(self):
        return self._tags

    @property
    def time(self):
        return self._time

    def extra_tags(self, extra_tags):
        self.tags.update(extra_tags)
        return self

    def as_dict(self):
        return {
            "measurement": self.name,
            "tags": self.tags,
            "time": self.time,
            "fields": self.values
        }

    def __str__(self):
        return "Metric(%s; %s; %s; %s)" % (self.name, self.time,
                                           self.values, self.tags)


def metric(name, value=1, tags=None):
    tags = tags if tags else {}
    values = {"value": float(value)}
    return _Metric(name, values, tags)


class _PublisherHandler(Thread):
    """
    This class executes operations inside the event loop scope
    """
    def __init__(self, publisher, interval, tags):
        Thread.__init__(self)
        self.daemon = True
        self.publisher = publisher
        self.interval = interval
        self.metrics = []
        self.tags = tags if tags else {}
        self.lock = RLock()
        self.timer = None

    def run(self):
        while True:
            time.sleep(self.interval)
            self.publish()

    def add_metrics(self, extra_metrics):
        self.lock.acquire(timeout=1)
        try:
            self.metrics.extend(extra_metrics)
        finally:
            self.lock.release()

    def publish(self):
        self.lock.acquire(timeout=1)
        try:
            metrics = self.metrics
            self.metrics = []
        finally:
            self.lock.release()

        count = len(metrics)
        if count > 0:
            log.info('Publishing %s metrics', count)
            formatted = map(lambda x: x.extra_tags(self.tags).as_dict(),
                            metrics)
            try:
                self.publisher.write_points([m for m in formatted])
            except:
                log.exception('Error publishing metrics')
                self.add_metrics(metrics)
        else:
            log.debug('No metrics to publish')


class MetricsRegistry:
    def __init__(self, publisher, interval, tags=None):
        self._handler = _PublisherHandler(publisher, interval, tags)

    def start(self):
        self._handler.start()

    def add_metric(self, metric):
        self.add_metrics([metric])

    def add_metrics(self, metrics):
        self._handler.add_metrics(metrics)
