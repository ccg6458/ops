from app.lib.extensions import db
from app.lib.http_res import BaseHttpException
import copy


class BaseModel(db.Model):
    success = 1
    __abstract__ = True

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            self.success=0

    def update_byId(self, id, newdata):
        self.query.filter_by(id=id).update(newdata)
        db.session.commit()

    def to_json(self):
        dict = copy.deepcopy(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
