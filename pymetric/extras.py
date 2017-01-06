import time

from pymetric.metrics import MetricsRegistry, metric


class MetricWsgiApp:
    def __init__(self, app, registry):
        self._app = app
        self._registry = registry = registry

    def __call__(self, environ, start_response):
        metrics = []

        def wrap_start_response(status, response_headers, exc_info=None):
            req_length = int(environ.get('CONTENT_LENGTH', 0))
            resp_length = 0
            for k, v in response_headers:
                if k.lower() == 'content-length':
                    resp_length = int(v)
                    break

            info = {'path_info': environ.get('PATH_INFO')}
            metrics.append(metric("request.length", value=req_length,
                                  tags=info))
            metrics.append(metric("response.length", value=resp_length,
                                  tags=info))
            info['status_code'] = int(status.split()[0])
            metrics.append(metric("request.count", value=1,
                                  tags=info))

            return start_response(status, response_headers, exc_info)

        start = time.perf_counter()

        response = self._app(environ, wrap_start_response)

        elapsed_secs = (time.perf_counter() - start) * 1000
        metrics.append(metric("request.duration.ms", elapsed_secs))

        self._registry.add_metrics(metrics)
        return response


def instrument_flask(flask_app, registry):
    flask_app.wsgi_app = MetricWsgiApp(flask_app.wsgi_app, registry)
    return flask_app


def create_registry(influx, interval=5, tags=None):
        return MetricsRegistry(influx, interval, tags)
