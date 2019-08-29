from app.lib.extensions import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, TEXT
from sqlalchemy.orm import foreign, remote, relationship
from . import BaseModel
from .user import UserModel
from .business import BusinessModel
import copy
from datetime import datetime


class TaskModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.create_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        super(TaskModel, self).__init__(*args, **kwargs)

    __tablename__ = 'task'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    business_id = db.Column(Integer, ForeignKey(BusinessModel.id))
    schedule = db.Column(String(64))
    shell = db.Column(TEXT)
    comment = db.Column(String(128))
    business = relationship("BusinessModel", backref="task")
    create_time = db.Column(String(64))

    def to_json(self):
        dict = copy.deepcopy(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        dict['business'] = self.business.name
        dict['ip'] = self.business.host
        return dict
