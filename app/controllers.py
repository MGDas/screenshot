from celery.result import AsyncResult
from flask import request, Blueprint, jsonify

from app.models import RunningTask
from app.tasks import celery as celery_app
from app.tasks import make_screen_task
from app.database import db


router = Blueprint('screenshot', __name__)


@router.route('/screenshot/', methods=['POST'])
def make_screenshot_websites():
    task = make_screen_task.delay(request.json.get('urls'))
    return jsonify({'task_id': task.id}), 200


@router.route('/status/<task_id>/', methods=['GET'])
def get_status_task(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        'task_id': task_id,
        'task_status': task_result.status
    }
    return jsonify(result), 200


@router.route('/screenshot/<task_id>/', methods=['GET'])
def get_screenshot_list(task_id):
    running_task = db.session.query(RunningTask).filter_by(task_id=task_id).scalar()
    response_data = running_task.serialize if running_task is not None else {}
    return jsonify(response_data), 200

