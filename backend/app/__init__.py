from flask import Flask, redirect, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()  # 初始化JWT扩展
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 配置CORS - 推荐使用flask-cors库的方式，更可靠
    CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:8080",  # 允许的前端源
            "supports_credentials": True,  # 允许跨域携带cookie（如果需要）
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 允许的方法
            "allow_headers": ["Content-Type", "Authorization"]  # 允许的请求头
        }
    })
    app.json.ensure_ascii = False  # 解决中文乱码问题
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate = Migrate(app, db)  # 初始化迁移扩展
    jwt.init_app(app)

    # 蓝图注册
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    from .routes.user import users_bp
    app.register_blueprint(users_bp, url_prefix='/user')

    # 根路径重定向
    @app.route('/')
    def index():
        return redirect(url_for('tasks.get_tasks'))

    # 处理所有OPTIONS请求，返回200状态码
    @app.route('/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        return make_response('', 200)

    return app
