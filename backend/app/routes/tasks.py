from flask import Blueprint, jsonify, request
from ..models import Task, db, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint("tasks", __name__)

# 返回统一格式
def resp_success(msg="成功", data=None):
    return jsonify({"code": 0, "msg": msg, "data": data}), 200

def resp_error(msg="失败"):
    return jsonify({"code": 1, "msg": msg, "data": None}), 400

# 显示所有事项
@tasks_bp.route("/query/all", methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    tasks = user.tasks
    return resp_success(data=[
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "due_date": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            "completed": t.completed,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S") if t.created_at else None,
            "user_id": t.user_id
        } for t in tasks])

# 获取单个任务
@tasks_bp.route('/query/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return resp_error("Task not found"), 404
    return resp_success(data={
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        "completed": task.completed,
        "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if task.created_at else None,
        "user_id": task.user_id
    })

# 添加事项
@tasks_bp.route('/add', methods=['POST'])
@jwt_required()
def addTask():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    # 判断是否添加为空
    if not data or "title" not in data:
        return resp_error("请输入任务标题")

    task = Task(
        title=data["title"],  # title必填项
        description=data.get('description'),
        priority=data.get('priority', "低"),
        due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else None,
        completed=data.get('completed'),
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return resp_success(data={
        "id": task.id,
        "title": task.title,  # title必填项
        "description": task.description,
        "priority": task.priority,
        "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        "completed": task.completed,
        "user_id": task.user_id
    }, msg="任务添加成功")

# 更新任务事项
@tasks_bp.route('/update/<int:task_id>', methods=['PUT'])
@jwt_required()
def updateTask(task_id):
    user_id = int(get_jwt_identity())
    # 先查询待更改任务
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return resp_error('任务不存在')

    data = request.get_json()
    if not data:
        return resp_error('请求不能为空')
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.priority = data.get("priority", task.priority)
    if data.get('due_date'):
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return resp_success(data={
        "id": task.id,
        "title": task.title,  # title必填项
        "description": task.description,
        "priority": task.priority,
        "due_date": task.due_date.strftime('%Y-%m-%d'),
        "completed": task.completed,
        "user_id": task.user_id
    },msg="任务更新成功")

# 删除任务
@tasks_bp.route("/delete/<int:task_id>", methods=['DELETE'])
@jwt_required()
def deleteTask(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return resp_error("任务不存在")
    db.session.delete(task)
    db.session.commit()
    return resp_success("任务删除成功")




