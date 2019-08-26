from app.lib.extensions import db
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import foreign, remote, relationship
from . import BaseModel


class SideBarModel(BaseModel):
    __tablename__ = 'sidebar'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    index = db.Column(Integer)
    icon = db.Column(String(32))
    tab = db.Column(String(32))
    routelink = db.Column(String(32))
    is_super = db.Column(Integer)

