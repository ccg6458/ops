from . import SecurityResource
from flask import request
from app.form.user import UserForm
from app.model.user import UserModel
from app.api.log import Log
from flask_login import login_required, current_user


class UserApi(SecurityResource):
    module = 'user'
    cloumn = ['name', 'email', 'status']
    super_api = True

    def get_form_data(self):
        form = UserForm(request.form, csrf=False)
        name = form.name.data
        email = form.email.data
        status = form.status.data
        value_list = [name, email, status]
        return value_list

    def get(self, id=None, tag=None):
        super(UserApi, self).get()
        if tag == 'all':
            user_list = []
            query = UserModel.query.all()
            for data in query:
                user_list.append(data.to_json())
            return self.render_json(data=user_list)
        userid = id or current_user.id
        data = UserModel.query.filter_by(id=userid).first().to_json()
        return self.render_json(data=data)

    def post(self):
        super(UserApi, self).post()
        code=0
        value_list = self.get_form_data()
        userinfo = dict(zip(self.cloumn, value_list))
        userinfo['password'] = request.form.get('password')
        user = UserModel(**userinfo)
        user.save()
        if not user.success:
            return self.render_json(code=1003)
        self.log(name=userinfo['name'])
        return self.render_json()

    def put(self, id):
        super(UserApi, self).put()
        value_list = self.get_form_data()
        userinfo = dict(zip(self.cloumn, value_list))
        UserModel.query.filter_by(id=id).update(userinfo)

        return self.render_json()

    def delete(self, id=None):
        super(UserApi, self).delete()
        user = UserModel.query.filter_by(id=id)
        name = user.first().name
        user.delete()
        self.log(name=name)
        return self.render_json()
