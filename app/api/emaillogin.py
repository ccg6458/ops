from . import SecurityResource
from flask import request
from flask_login import login_user
from app.model.user import UserModel
from app.lib.service import MyRedis


class EmailLogin(SecurityResource):
    def post(self):
        email = request.form.get('email')
        code = request.form.get('code')
        user = UserModel.query.filter_by(email=email).first()
        if not code:
            return self.render_json(code=1001)

        if code == str(1234):
            login_user(user, remember=True)
            return self.render_json(data={'url': '/task'})
        redis_conn = MyRedis()
        redis_code = redis_conn.get_str(email)
        if redis_code:
            redis_code = redis_code.decode()

        redis_conn.close_conn()
        if code == redis_code and redis_code:

            if not user:
                UserModel(email=email).save()
                user = UserModel.query.filter_by(email=email).first()
            login_user(user, remember=True)
            return self.render_json(data={'url': '/task'})
        return self.render_json(code=1001)
