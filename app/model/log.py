from app.lib.extensions import db
from app.lib.service import now
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import foreign, remote, relationship
from . import BaseModel
from .user import UserModel
from .business import BusinessModel
import copy


class LogModel(BaseModel):
    __tablename__ = 'log'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    username = db.Column(String(32))
    behavior = db.Column(String(128))
    create_time = db.Column(String(64), default=now)

    def to_json(self):
        dict = copy.deepcopy(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
