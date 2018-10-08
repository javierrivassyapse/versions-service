# -*- coding: utf-8 -*-
""" A Flask plugin for structured logging. """

import structlog

from flask import Flask, helpers
from typing import Optional


class FlaskStructlog:
    """FlaskStructlog

    A flask extension for patching the builtin Flask logger with a structlogger.
    """

    def __init__(self, app: Optional[Flask]=None, *args, **kwargs) -> None:
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """init_app

        Patches the builtin Flask logger and replaces it with a structlog logger.

        :param app:
            The Flask app for which to patch the logger.
        """
        if not structlog.is_configured():
            app.logger.warning(
                'The structlog module is not configured yet. Refusing to patch the Flask logger.')
            return None

        self._patch_flask_logger(app)

    def _patch_flask_logger(self, app):
        """_patch_flask_logger

        Replaces the builtin flask logger with a structured logger.

        :param app:
            The Flask app for which to patch the logger
        """
        structured_logger = structlog.get_logger('flask.app')

        def structlogger(self):
            return structured_logger

        setattr(app.__class__, 'logger', helpers.locked_cached_property(structlogger))

        if app.logger is not structured_logger:
            app.logger.warning(
                'The FlaskStructlog extension was unable to patch the builtin Flask logger. This '
                'probably means that a message was logged before the extension was initialized.'
            )
