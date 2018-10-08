# -*- coding: utf-8 -*-
""" Metrics helpers. """

from contextlib import contextmanager

from .extensions import statsd


@contextmanager
def measure(base_metric: str):
    """measure

    A context manager for measuring runtime, call count, success count, and
    errors for a yielded block of code, and reporting those metrics to statsd.

    .. code-block python
        with measure('my_service.my_module.something_interesting'):
            sleep(10)
            raise RuntimeError('Too slow!')

        # StatsD:
        #  - my_service.my_module.something_interesting.runtime: 10s
        #  - my_service.my_module.something_interesting.successes: +0
        #  - my_service.my_module.something_interesting.errors.RuntimeError: +1
        #  - my_service.my_module.something_interesting.calls: +1
    """
    with statsd.pipeline() as pipe:
        with pipe.timer(f'{base_metric}.runtime') as timer:
            try:
                yield pipe, timer
                pipe.incr(f'{base_metric}.successes')
            except Exception as ex:
                pipe.incr(f'{base_metric}.errors.{ex.__class__.__name__}')
                raise
            finally:
                pipe.incr(f'{base_metric}.calls')
