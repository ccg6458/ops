from app.lib.extensions import db
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import foreign, remote, relationship
from . import BaseModel
from .user import UserModel
import copy



class BusinessModel(BaseModel):
    __tablename__='business'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name=db.Column(String(32),default='test')
    host=db.Column(String(32),default='127.0.0.1')
    user = relationship("UserModel", backref="business",secondary='permission')


    def to_json(self):
        dict = copy.deepcopy(self.__dict__)

        if "user" in dict:
            del dict['user']
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def to_id_name_json(self):
        dict = copy.deepcopy(self.__dict__)

        if "user" in dict:
            del dict['user']
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        del dict["host"]
        dict["business_id"]=self.id
        del dict['id']
        return dict

class PermissionModel(BaseModel):
    __tablename__ = 'permission'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(Integer, ForeignKey(BusinessModel.id))
    user_id = db.Column(Integer, ForeignKey(UserModel.id))