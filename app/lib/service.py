from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import Config
from app.lib.http_res import BaseHttpException
from app.lib.script import Mymysql
import paramiko, redis
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random, datetime, fcntl


class ShellExec():
    """
    利用paramiko实现远程ssh功能
    """

    def __init__(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh = ssh

    def exec(self, ip, shell):
        keyfile = Config.PRIVATE_KEY
        private_key = paramiko.RSAKey.from_private_key_file(keyfile)
        self.ssh.connect(hostname=ip, port=22, username="root", pkey=private_key)
        stdin, stdout, stderr = self.ssh.exec_command(shell)
        result = stdout.read().decode()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cron_info = "主机ip  :{}\n执行时间: {}\n当前任务: {}".format(str(ip), now, shell)
        self.log_to_file(cron_info, result)
        self.ssh.close()

    def log_to_file(self, cron_info, res):
        filename = Config.APP_DIR + '/logs/cron-' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
        with open(filename, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.writelines(cron_info + '\n')
            f.writelines(res + '\n')
            f.writelines('----------------------------------------\n')
            fcntl.flock(f, fcntl.LOCK_UN)


class CronJob():
    """
    利用apscheduler实现定时任务功能
    """

    def __new__(cls, *args, **kwargs):
        """
        实现单例模式
        :param args:
        :param kwargs:
        :return:
        """

        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        self.sched = BackgroundScheduler()

    def job_fun(self, ip, shell):
        cmd = ShellExec()
        cmd.exec(ip, shell)

    def add_cronjob(self, schedule, shell, id, ip):
        self.sched.add_job(self.job_fun, CronTrigger.from_crontab(schedule), args=[ip, shell], id=id,
                           replace_existing=True,max_instances=5)

    def remove_crontjob(self, id):
        self.sched.remove_job(str(id))

    def init_cronjob(self, list):
        for data in list:
            self.add_cronjob(data['schedule'], data['shell'], str(data['id']), data['ip'])

    def exec_sql(self, id, sql_list):

        db = Mymysql()
        finish_sql = 'update test.workorder set finish=1 where id=' + id
        for sql in sql_list:
            db.execute_sql(sql)
        db.execute_sql(finish_sql)
        db.close()

    def add_sql_job(self, id, sql):
        self.sched.add_job(self.exec_sql, args=[id, sql])

    def start(self, list):
        self.init_cronjob(list)
        self.sched.start()


class MyRedis():
    def __init__(self):
        self.conn = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD)

    def set_str(self, key, value, ex=120):
        self.conn.set(key, value, ex)

    def get_str(self, key):
        val = self.conn.get(key)
        return val

    def close_conn(self):
        self.conn.close()


class SendMsg():
    def __init__(self):
        self.smtp = smtplib.SMTP_SSL(Config.MAIL_HOST, 465)
        self.mail_user = Config.MAIL_USER
        self.mail_host = Config.MAIL_HOST
        self.mail_password = Config.MAIL_PASSWORD

    def generate_code(self):
        code = ''
        for i in range(4):
            j = random.randrange(0, 4)
            if j == 1:
                a = random.randrange(0, 10)
                code = code + str(a)
            elif j == 2:
                a = chr(random.randrange(65, 91))
                code = code + a
            else:
                a = chr(random.randrange(97, 121))
                code = code + a
        return code

    def content(self, code):
        message = """本次登陆验证码为: %s,有效期两分钟。
                """ % (code)
        email_content = MIMEText(message)
        return email_content


    def send(self, email_address, code):
        email = MIMEMultipart()
        email['from'] = self.mail_user
        email['to'] = email_address
        email['subject'] = '登陆验证码'
        email.attach(self.content(code))
        self.smtp.login(self.mail_user, self.mail_password)
        self.smtp.sendmail(self.mail_user, email_address, email.as_string())
