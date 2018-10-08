# -*- coding: utf-8 -*-
""" A flask extension for configuring Celery. """

import flask
from celery import Celery


class FlaskCelery(Celery):
    """ An extension for executing Celery tasks with the Flask application context. """

    def __init__(self, *args, **kwargs):  # noqa
        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        """ Patches the basecelery Task class to provide Flask context. """
        _celery = self
        TaskBase = self.Task  # noqa

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        """ Initializes the application with the given config. """
        self.app = app
        self.config_from_object(app.config)
