from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):  
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at =request_body["completed_at"]
        )
    db.session.add(new_task)
    db.session.commit()

    return ({"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }}, 201)



@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()

    return ({
    "details": f'Task {task_id} "{task.title}" successfully deleted'
    }, 200)

