from . import SecurityResource
from app.model.log import LogModel
from sqlalchemy import text
from flask import request


class Log(SecurityResource):
    super_api = True

    def get(self):
        super(Log, self).get()
        args = request.args
        pageSize = int(args.get('pageSize'))
        pageNum = int(args.get('pageNum'))
        offsetNum = (pageNum - 1) * pageSize if pageSize > 1 else 0
        total = len(LogModel.query.all())
        data = {}
        log_list = []
        logs = LogModel.query.order_by(LogModel.create_time.desc()).limit(pageSize).offset(offsetNum).all()
        for log in logs:
            log_list.append(log.to_json())
        data['total'] = total
        data['log'] = log_list

        return self.render_json(data=data)
