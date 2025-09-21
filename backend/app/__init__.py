from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False  # 解决中文乱码问题
    app.config.from_object("config.Config")

    db.init_app(app)

    # 蓝图注册
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    # 根路径重定向
    @app.route('/')
    def index():
        return redirect(url_for('tasks.getTasks'))

    return app
