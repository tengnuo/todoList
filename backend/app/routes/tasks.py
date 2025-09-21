from flask import Blueprint, jsonify, request
from ..models import Task, db
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__)

# 显示所有事项
@tasks_bp.route("/query/all", methods=['GET'])
def getTasks():
    tasks = Task.query.all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "priority": t.priority,
            "due_date": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            "completed": t.completed,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S") if t.created_at else None,
            "user_id": t.user_id
        } for t in tasks
    ]), 200

# 获取单个任务
@tasks_bp.route('/query/<int:task_id>', methods=['GET'])
def getTask(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        "completed": task.completed,
        "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S") if task.created_at else None,
        "user_id": task.user_id
    }), 200

# 添加事项
@tasks_bp.route('/add', methods=['POST'])
def addTask():
    data = request.get_json()
    # 判断是否添加为空
    if not data or "title" not in data:
        return jsonify({"error": "请输入任务标题"})

    task = Task(
        title = data["title"],  # title必填项
        description = data.get('description'),
        priority = data.get('priority', "低"),
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d') if data.get('due_date') else None,
        completed = False,
        user_id = 1
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "message": "Task added",
        "id": task.id
    }), 201

# 更新任务事项
@tasks_bp.route('/update/<int:task_id>', methods=['PUT'])
def updateTask(task_id):
    # 先查询待更改任务
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": 'Task not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": '请求不能为空'}), 400
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.priority = data.get("priority", task.priority)
    if data.get('due_date'):
        task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return jsonify({"message": "任务更新成功"}), 200

# 删除任务
@tasks_bp.route("/delete/<int:task_id>", methods=['DELETE'])
def deleteTask(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "删除成功"}), 200




