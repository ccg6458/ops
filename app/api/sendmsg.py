from app.api import SecurityResource
from app.lib.service import SendMsg, MyRedis
from app.lib.extensions import cron
from flask import request


class SendMsgApi(SecurityResource):
    def post(self):
        email_address = request.form.get('email')

        if not self.check_email(email_address):
            return self.render_json(code=1005)
        redis_conn = MyRedis()
        if redis_conn.get_str(email_address):
            return self.render_json(code=1004)
        redis_conn.close_conn()
        cron.sched.add_job(self.send, args=[email_address])
        return self.render_json()

    def check_email(self, email_address):
        l1 = email_address.split('@')
        if len(l1) == 2 and l1[1] == 'mifengkong.cn':
            return True
        return False

    def send(self, email_address):
        mail = SendMsg()
        code = mail.generate_code()
        redis_conn = MyRedis()
        redis_conn.set_str(email_address, code)
        redis_conn.close_conn()
        cron.sched.add_job(mail.send, args=[email_address, code])
