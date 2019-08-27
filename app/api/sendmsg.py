from app.api import SecurityResource
from app.lib.service import SendMsg, MyRedis
from flask import request


class SendMsgApi(SecurityResource):
    def post(self):
        email_address = request.form.get('email')

        if not self.check_email(email_address):
            return self.render_json(code=1005)

        mail = SendMsg()
        redis_conn = MyRedis()
        if redis_conn.get_str(email_address):
            return self.render_json(code=1004)
        code = mail.generate_code()
        redis_conn.set_str(email_address, code)
        redis_conn.close_conn()
        mail.send(email_address, code)
        return self.render_json()

    def check_email(self, email_address):
        l1 = email_address.split('@')
        if len(l1) == 2 and l1[1] == 'mifengkong.cn':
            return True
        return False
