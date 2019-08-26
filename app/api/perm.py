from . import SecurityResource
from flask import request
from flask_login import login_required
from app.model.user import UserModel
from app.model.business import BusinessModel
import json


class PermApi(SecurityResource):
    super_api = True

    def get(self, id):
        super(PermApi, self).get()
        user = UserModel.query.filter_by(id=id).first()
        user.business
        res = user.to_json()
        return self.render_json(data=res)
