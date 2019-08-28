from app.lib.extensions import db
from sqlalchemy import String, Integer, ForeignKey,DateTime,TEXT
from sqlalchemy.orm import relationship
from . import BaseModel
from .user import UserModel
import copy,datetime


class WorkOrderModel(BaseModel):
    type_msg={
        1: 'sql执行',
        2: '域名相关',
        3: '其他'
    }

    __tablename__ = 'workorder'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    type = db.Column(Integer)
    name = db.Column(String(128))
    sql = db.Column(TEXT)
    database = db.Column(String(32))
    audit = db.Column(Integer,default=0)
    finish = db.Column(Integer,default=0)
    result = db.Column(String(256))
    user_id = db.Column(Integer, ForeignKey(UserModel.id))
    userinfo = relationship("UserModel", backref="work")
    create_time = db.Column(DateTime,default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    comment = db.Column(String(64))

    def to_json(self):
        dict = copy.deepcopy(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        dict['username']=self.userinfo.name if self.userinfo.name else self.userinfo.email.split('@')[0]
        del dict['user_id']
        return dict

