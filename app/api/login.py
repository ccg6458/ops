from . import SecurityResource
from flask import request
from flask_login import login_user, logout_user
from app.model.user import UserModel
from werkzeug.security import check_password_hash


class Login(SecurityResource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return self.render_json(code=1002)
        password_hash = user.password
        if check_password_hash(password_hash, password):
            login_user(user,remember=True)
            return self.render_json(data={'url': '/task'})
        return self.render_json(code=1001)


class Logout(SecurityResource):
    def get(self):
        logout_user()
        return self.render_json()
