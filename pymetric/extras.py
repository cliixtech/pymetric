import time

from pymetric.metrics import MetricsRegistry, metric


class MetricWsgiApp:
    def __init__(self, app, influx, tags, interval):
        self._app = app
        self._registry = MetricsRegistry(influx, interval, tags)
        self._registry.start()

    def __call__(self, environ, start_response):
        metrics = []
        start = time.perf_counter()

        def wrap_start_response(status, response_headers, exc_info=None):
            code = {'wsgi.status_code': int(status.split()[0])}
            metrics.append(metric("wsgi.requests", value=1,
                                  tags=code))
            return start_response(status, response_headers, exc_info)

        response = self._app(environ, wrap_start_response)

        elapsed_secs = (time.perf_counter() - start) * 1000
        metrics.append(metric("wsgi.duration.ms", elapsed_secs))

        self._registry.add_metrics(metrics)
        return response


def instrument_flask(flask_app, influx, tags=None, interval=5):
    flask_app.wsgi_app = MetricWsgiApp(flask_app.wsgi_app, influx, tags,
                                       interval)
    return flask_app
