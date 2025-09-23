from flask import Blueprint, jsonify, request
from ..models import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint("users", __name__)

# 用户注册
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({
            "error": "用户名和密码不能为空"
        }), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({
            "error": "用户名已存在"
        }), 400
    user = User(username = data["username"])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "用户注册成功"
    }), 200

# 用户登录
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "请输入用户名"}), 400
    if "password" not in data:
        return jsonify({"error": "请输入密码"}), 400
    user = User.query.filter_by(username = data["username"]).first()
    if not user:
        return jsonify({"error": "用户不存在"}), 400

    if not user.check_password(data['password']):
        return jsonify({"error": "密码不正确"}), 400

    # 创建 JWT token,有效期一天
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify({ "access_token": access_token}), 200

# 查看个人信息
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    userId = int(get_jwt_identity())
    user = User.query.get(userId)
    if not user:
        return jsonify({"error": '用户不存在'}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "gender": user.gender,
        "age": user.age
    }), 200

# 信息更新
@users_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user_profile():
    userId = int(get_jwt_identity())
    user = User.query.get(userId)

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求不能为空"}), 400

    user.username = data.get("username", user.username)
    user.avatar = data.get("avatar", user.avatar)
    user.age = data.get("age", user.age)
    user.gender = data.get("gender", user.gender)

    db.session.commit()

    return jsonify({"message": "个人信息修改成功"}), 200

# 修改密码
@users_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()
    old_pw = data.get("old_password")
    new_pw = data.get("new_password")
    if not old_pw or not new_pw:
        return jsonify({"error": "请输入旧密码或新密码"})
    if not check_password_hash(user.password_hash, old_pw):
        return jsonify({"error": "旧密码不正确"})
    user.password_hash = generate_password_hash(new_pw)
    db.session.commit()
    return jsonify({"message": "密码修改成功"})

