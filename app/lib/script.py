import pymysql

import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/Users/mc/.ssh/id_rsa')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname='119.23.161.45', port=22, username="root", pkey=private_key)

stdin, stdout, stderr = ssh.exec_command('ls -l /')

result = stdout.read().decode()

ssh.close()


class Mymysql():
    success = 1

    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "mifeng888", "test")
        self.cursor = self.db.cursor()

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.db.commit()
            return True, data
        except Exception as e:
            self.success = 0
            self.rollback()
            return False, e.args

    def rollback(self):
        self.db.rollback()

    def update_by_sql(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        self.db.close()
