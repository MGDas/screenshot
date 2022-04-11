from flask import url_for, request

from app.database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


task_screenshot = db.Table(
    'task_screenshot',
    db.Column('running_task_id', db.Integer, db.ForeignKey('running_task.id')),
    db.Column('screenshot_id', db.Integer, db.ForeignKey('screenshot.id')),
)


class RunningTask(BaseModel):
    __tablename__ = 'running_task'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(36), unique=True, index=True)

    screenshots = db.relationship('Screenshot', secondary=task_screenshot, backref='running_tasks')

    @property
    def serialize(self):
        return {
            "task_id": self.task_id,
            "screenshots": [screen.get_image_url for screen in self.screenshots]
        }

    def __str__(self):
        return self.task_id


class Screenshot(BaseModel):
    __tablename__ = 'screenshot'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300), unique=True, index=True)
    img = db.Column(db.String(30))

    def __str__(self):
        return self.url

    @property
    def get_image_url(self):
        path_to_file = url_for('static', filename=f'uploads/{self.img}').lstrip("/")
        return "".join([request.host_url, path_to_file])
