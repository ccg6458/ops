from flask import Flask, g
from flask_restful import Api
from app.config import Config
from app.api.user import UserApi
from app.api.perm import PermApi
from app.api.login import Login, Logout
from app.api.sidebar import SideBarApi
from app.api.business import BusinessApi
from app.api.task import TaskApi
from app.api.log import Log
from app.api.sendmsg import SendMsgApi
from app.api.emaillogin import EmailLogin
from app.api.workorder import WorkOrderApi

from app.model.user import UserModel
from app.model.task import TaskModel
from app.lib.extensions import CronJob

from app.lib.extensions import db, login_manager, cron
from flask_cors import CORS, cross_origin
from flask_login import login_required


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_url(app)
    CORS(app, supports_credentials=True)
    register_cron(app)

    return app


def register_extensions(app):
    db.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.query.get(user_id)

    login_manager.init_app(app)

    return app


def register_url(app):
    api = Api(app)
    api.add_resource(UserApi, '/test/', '/test/<string:tag>', '/test/<int:id>', endpoint='user')
    api.add_resource(PermApi, '/perm/<int:id>', endpoint='perm')
    api.add_resource(Login, '/login', endpoint='login')
    api.add_resource(Logout, '/logout', endpoint='logout')
    api.add_resource(SideBarApi, '/sidebar', endpoint='sidebar')
    api.add_resource(BusinessApi, '/business', '/business/<string:tag>', '/business/<string:tag>/<int:id>',
                     '/business/modify/<int:id>', endpoint='business')
    api.add_resource(TaskApi, '/task', '/task/<int:id>', endpoint='task')
    api.add_resource(Log, '/log', endpoint='audit')
    api.add_resource(SendMsgApi, '/sendmsg', endpoint='sendmsg')
    api.add_resource(EmailLogin, '/emaillogin', endpoint='emaillogin')
    api.add_resource(WorkOrderApi, '/work', '/work/<string:tag>', endpoint='work')

    return app


def register_cron(app):
    task_list = []
    with app.app_context():
        tasks = TaskModel.query.all()
        for task in tasks:
            task_list.append(task.to_json())
    cron.start(task_list)
    return app
