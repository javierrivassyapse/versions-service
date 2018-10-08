# -*- coding: utf-8 -*-
""" Create an application instance. """

from versions_service.app import celery, create_app  # noqa
from versions_service.settings import Config

app = create_app(config_object=Config)
