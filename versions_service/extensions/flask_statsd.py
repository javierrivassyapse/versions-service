# -*- coding: utf-8 -*-
""" Metrics extension for measuring application performance with statsd. """

from statsd import StatsClient


class FlaskStatsd(StatsClient):
    """ A flask extension for wrapping statsd. """

    def __init__(self, *args, **kwargs):  # noqa
        super(FlaskStatsd, self).__init__(*args, **kwargs)

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def init_app(self, app):
        """ Initializes defauls statsd configuration. """
        app.config.setdefault('STATSD_HOST', 'localhost')
        app.config.setdefault('STATSD_PORT', 8125)
        app.config.setdefault('STATSD_MAX_UDP_SIZE', 512)
        app.config.setdefault('STATSD_IPV6', False)

        self.__init__(
            host=app.config.get('STATSD_HOST'),
            port=app.config.get('STATSD_PORT'),
            prefix=app.config.get('STATSD_PREFIX'),
            maxudpsize=app.config.get('STATSD_MAX_UDP_SIZE'),
            ipv6=app.config.get('STATSD_IPV6'))
