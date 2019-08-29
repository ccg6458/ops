from flask_restful import Resource
from flask_login import current_user
from flask import current_app, jsonify, request
from app.lib.http_res import Code, BaseHttpException
from app.model.log import LogModel
from app.model.sidebar import SideBarModel
import json


class ApiResource(Resource):
    def __init__(self):
        pass

    @staticmethod
    def render_json(code=0, message='', data=[]):
        return ApiResource.json(code=code, message=message, data=data)

    @staticmethod
    def json(code=0, message=None, data=[]):

        if code and code not in Code.code_msg:
            current_app.logger.error('unknown code %s' % (code))

        if code in Code.code_msg and not message:
            message = Code.code_msg[code]

        return jsonify({
            'code': code,
            'message': message,
            'data': data,
        })


class Access:
    def __init__(self):
        pass

    @staticmethod
    def is_login():
        return current_user.is_authenticated

    @staticmethod
    def is_super_role():
        if current_user.is_super():
            return True
        return False

    # @staticmethod
    # def is_allow(action, module=None):
    #     module_white_list = ['sidebar']
    #
    #     print(current_user.to_json()['perm'])
    #
    #     if module in module_white_list:
    #         return True
    #     if current_user.is_super():
    #         return True
    #
    #     current_user.perm
    #     if Access.resource(action, module) in current_user.to_json()['perm']:
    #         return True
    #     return False

    # @staticmethod
    # def resource(action, module=None):
    #     return "{}_{}".format(str(action), module)
    @staticmethod
    def resource(task_id):
        return task_id


class SecurityResource(ApiResource):
    super_api = False
    module = None
    action = None
    actions = []
    action_msg = {
        'create': '创建',
        'update': '更新',
        'delete': '删除'
    }
    module_msg = {
        'user': '用户',
        'task': '任务',
        'order': '工单'
    }

    # def get_super_api(self):
    #     link = '/' + request.endpoint
    #     sidebar = SideBarModel.query.filter_by(routelink=link).first()
    #     return True if sidebar.is_super == 1 else False

    def log(self, action=None, module=None, info=None, before=None, after=None):
        if not action:
            action = self.action
        if not module:
            module = self.module
        username = current_user.name if current_user.name else current_user.email.split('@')[0]
        action_cn = self.action_msg[action]
        module_cn = self.module_msg[module]
        if action == 'create' or action == 'delete':
            behavior = "{}{} {}".format(action_cn, module_cn, info)
        if action == 'update':
            behavior = "{}{}  {} 修改至 {}".format(action_cn, module_cn, before, after)
        log = LogModel(username=username, behavior=behavior)
        log.save()

    def get(self):
        self.action = 'get'
        return self.validator()

    def post(self):
        self.action = 'create'
        return self.validator()

    def put(self):
        self.action = 'update'
        return self.validator()

    def delete(self):
        self.action = 'delete'
        return self.validator()

    def validator(self):
        if not Access.is_login():
            raise BaseHttpException(code=1000)

        if self.super_api:
            if not Access.is_super_role():
                raise BaseHttpException(code=2000)

                # if not Access.is_allow(action=self.action, module=self.module):
                #     raise BaseHttpException(code=2001)
