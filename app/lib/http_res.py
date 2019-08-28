from werkzeug.exceptions import HTTPException
import json


class Code():
    #: 没有消息就是好消息
    Ok = 0

    #: ----------------------- 1xxx 用户相关错误 -----------------
    unlogin = 1000

    #: 密码错误
    error_pwd = 1001

    #: 用户不存在
    not_user = 1002

    #: 该用户已存在
    exists_user = 1003

    #: 重复发送验证码
    repeat_code = 1004

    #: 邮箱格式错误
    error_mail = 1005

    #: ----------------------- 2xxx 权限相关错误 -----------------
    only_super = 2000
    not_permission = 2001

    #: ----------------------- 3xxx sql相关错误 -----------------
    sql_execute_error = 3000

    code_msg = {
        unlogin: '请先登陆',
        error_pwd: '密码错误',
        not_user: '用户不存在',
        repeat_code: '请不要重复发送验证码',
        error_mail: '邮箱格式错误',
        exists_user: '该用户已存在',
        only_super: '非管理员无权操作',
        not_permission: '没有该资源权限',
        sql_execute_error: '数据库执行错误'

    }


class BaseHttpException(HTTPException):
    def __init__(self, code=0, message='', data=[],
                 headers=None):
        self.data = {'code': code,
                     'message': message if message else Code.code_msg.get(code, '未知错误'),
                     'data': data}
        super(BaseHttpException, self).__init__(None)

    def get_body(self, environ=None):
        body = dict(
            message='',
            code=200,
            data=self.data
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]
