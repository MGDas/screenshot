import os

from celery import Celery
from flask import Flask
from flask_migrate import Migrate

from app.database import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    import app.controllers as views

    app.register_blueprint(views.router)

    return app


def make_celery():
    celery = Celery()
    celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with create_app().app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
