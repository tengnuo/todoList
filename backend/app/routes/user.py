from flask import Blueprint, jsonify, request
from ..models import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime

users_bp = Blueprint("users", __name__)

# 返回统一格式
def resp_success(msg="成功", data=None):
    return jsonify({"code": 0, "msg": msg, "data": data}), 200

def resp_error(msg="失败"):
    return jsonify({"code": 1, "msg": msg, "data": None}), 400

# 用户注册
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return resp_error('用户名和密码不能为空')
    if User.query.filter_by(username=data["username"]).first():
        return resp_error('用户名已存在')
    user = User(username=data["username"])
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
    return jsonify({"token": access_token}), 200

# 查看个人信息
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    userId = int(get_jwt_identity())
    user = User.query.get(userId)
    if not user:
        return jsonify({"error": '用户不存在'}), 404

    birth_date_str = user.birth_date.strftime("%Y-%m-%d") if user.birth_date else ""

    return resp_success(data={
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "gender": user.gender,
        "birth_date": birth_date_str
    })

# 信息更新
@users_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_user_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    data = request.get_json()
    if not data:
        return jsonify({"error": "请求不能为空"}), 400

    # 取要保存的用户名（保留原值作为默认）
    new_username = data.get("username", user.username)
    if isinstance(new_username, str):
        new_username = new_username.strip()
    else:
        return resp_error('用户名格式不正确')

    # 用户名长度校验
    if new_username == "":
        return resp_error('用户名不能为空')
    if len(new_username) > 64:
        return resp_error("用户名长度不能超过64字符")

    # 只有当用户名真的发生变化时才去查重；查重时排除当前用户
    if new_username != user.username:
        exists = User.query.filter(User.username == new_username, User.id != user_id).first()
        if exists:
            return resp_error('用户名已存在')

    # 解析出生日期
    if "birth_date" in data and data["birth_date"]:
        try:
            # 前端传格式 "YYYY-MM-DD"
            user.birth_date = date.fromisoformat(data["birth_date"])
        except ValueError:
            return resp_error('传入格式不正确')

    user.username = data.get("username", user.username)
    user.avatar = data.get("avatar", user.avatar)
    user.gender = data.get("gender", user.gender)

    db.session.commit()

    return resp_success(msg="个人信息修改成功")

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

