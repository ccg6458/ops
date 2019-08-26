from app.lib.extensions import db
from sqlalchemy import String, Integer
from werkzeug.security import generate_password_hash
from . import BaseModel
from flask_login import UserMixin
import copy


class UserModel(BaseModel, UserMixin):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(32))
    email = db.Column(String(32))
    status = db.Column(Integer,default=1)
    _password = db.Column(String(50))
    super = db.Column(Integer,default=0)

    @property
    def is_active(self):
        if self.status == 1:
            return True
        return False

    def is_super(self):
        if self.super == 1:
            return True
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, passwd):
        self._password = generate_password_hash(passwd)

    def to_json(self):
        dict = copy.deepcopy(self.__dict__)
        if "perm" in dict:
            action_list = []
            for obj in dict['perm']:
                action_list.append(obj.id)
            dict['perm'] = action_list
        del dict['_password']
        if "business" in dict:
            del dict['business']
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def get_name_from_email(self):
        name=self.email.split('@')[0]
        return name
