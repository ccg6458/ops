from app.lib.extensions import db
from sqlalchemy import String, Integer, ForeignKey,DateTime,TEXT
from sqlalchemy.orm import foreign, remote, relationship
from . import BaseModel
from .user import UserModel
from .business import BusinessModel
import copy,datetime


class TaskModel(BaseModel):
    __tablename__ = 'task'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(Integer, ForeignKey(BusinessModel.id))
    schedule = db.Column(String(64))
    shell = db.Column(TEXT)
    business = relationship("BusinessModel", backref="task")
    create_time = db.Column(DateTime,default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


    def to_json(self):
        dict = copy.deepcopy(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        dict['business']=self.business.name
        dict['ip'] = self.business.host
        return dict