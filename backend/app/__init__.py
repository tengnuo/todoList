from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()  # 初始化JWT扩展
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
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

    return app
