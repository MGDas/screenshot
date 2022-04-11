import os
from time import time

from app import db, make_celery
from app.models import Screenshot, RunningTask
from app.selenium import WebDriver


celery = make_celery()


def get_file_name():
    return f"{int(time() * 1000)}.png"


@celery.task(name="make_screen")
def make_screen_task(data: list):
    task_id = make_screen_task.request.id
    running_task = RunningTask(task_id=task_id)

    for url in data:
        screen = db.session.query(Screenshot).filter_by(url=url).first()

        if screen is None:

            filename = get_file_name()

            webdriver = WebDriver()
            webdriver.make_screen(url, filename)
            webdriver.close()

            screen = Screenshot(url=url, img=filename)

            db.session.add(screen)
            db.session.flush()

        running_task.screenshots.append(screen)

    db.session.add(running_task)
    db.session.commit()

