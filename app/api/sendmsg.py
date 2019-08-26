from app.api import SecurityResource
from app.lib.service import SendMsg, MyRedis
from flask import request


class SendMsgApi(SecurityResource):
    def post(self):
        mail = SendMsg()
        redis_conn = MyRedis()
        email_address = request.form.get('email')
        if redis_conn.get_str(email_address):
            return self.render_json(code=1004)
        code = mail.generate_code()
        redis_conn.set_str(email_address, code)
        redis_conn.close_conn()
        mail.send(email_address, code)
        return self.render_json()