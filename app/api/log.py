from . import SecurityResource
from flask_login import current_user
from app.model.log import LogModel


class Log(SecurityResource):

    super_api = True

    def get(self):
        super(Log, self).get()
        log_list = []
        if current_user.is_super():
            logs = LogModel.query.all()
            for log in logs:
                log_list.append(log.to_json())
            return self.render_json(data=log_list)


