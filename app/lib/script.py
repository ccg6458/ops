import pymysql


class  Mymysql():
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "mifeng888", "test")
        self.cursor=self.db.cursor()

    def select_by_sql(self,sql):
        pass

    def update_by_sql(self,sql):
        pass

    def insert_by_sql(self,sql):
        pass

    def delete_by_sql(self,sql):
        pass

    def close(self):
        self.db.close()


a=Mymysql()
a.test()

