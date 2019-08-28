import pymysql
from app.config import Config
import paramiko


class Mymysql():
    success = 1

    def __init__(self):
        mysql = Config.MYSQL_INFO
        self.db = pymysql.connect(mysql['url'], mysql['user'],
                                  mysql['password'], mysql['database'])
        self.cursor = self.db.cursor()

    def execute_one_sql(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.db.commit()
            return True, data
        except Exception as e:
            self.success = 0
            self.rollback()
            return False, e.args
    def batch_execute_sql(self,sql_list):
        try:
            for sql in sql_list:
                self.cursor.execute(sql)
        except Exception as e:
            self.rollback()
            return False,e.args
        else:
            self.db.commit()
            return True,''



    def rollback(self):
        self.db.rollback()

    def update_by_sql(self, sql):
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        self.db.close()
