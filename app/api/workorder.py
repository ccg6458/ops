from . import SecurityResource
from app.model.workorder import WorkOrderModel
from app.model.user import UserModel
from app.form.workorder import WorkOrderForm
from app.lib.script import Mymysql
from app.lib.http_res import BaseHttpException
from flask_login import current_user
from flask import request
from app.lib.extensions import cron


class WorkOrderApi(SecurityResource):
    cloumn = ['type', 'name', 'sql', 'comment']

    def get(self, tag=None):

        if tag:
            func = getattr(self, tag, 'database')
            return func()
        super(WorkOrderApi, self).get()

        work_list = []
        data = {}
        if current_user.is_super():
            works = WorkOrderModel.query.all()
            for work in works:
                work_list.append(work.to_json())
            data['super'] = 1
            data['work'] = work_list
            return self.render_json(data=data)

        query = UserModel.query.filter_by(id=current_user.id).first().work
        for work in query:
            work_list.append(work.to_json())
        data['super'] = 0
        data['work'] = work_list
        return self.render_json(data=data)

    def post(self):
        super(WorkOrderApi, self).post()
        db = Mymysql()
        form = WorkOrderForm(request.form, csrf=False)
        name = form.name.data
        sql = form.sql.data

        comment = form.comment.data
        database = form.database.data if form.database.data else 'test'
        value_list = [type, name, sql, comment]
        workinfo = dict(zip(self.cloumn, value_list))
        workinfo['type'] = 1
        flag, res = self.check_sql(sql)
        if flag == 1:
            # 自动审核
            workinfo['audit'] = 2
            workinfo['finish'] = 1
            self.batch_execute_sql(res)
        elif flag == 2:
            db.close()
            return self.render_json(code=3000, message='sql不合法')
        elif flag == 3:
            # 人工审核
            pass
        else:
            db.close()
            return self.render_json(code=9999, message='未知错误')
        db.close()
        workinfo['sql'] = ';\n'.join(res)
        workinfo['user_id'] = current_user.id
        work = WorkOrderModel(**workinfo)
        work.save()
        return self.render_json()

    def put(self, tag=None):
        if tag:
            func = getattr(self, tag, 'audit')
            id = request.form.get('auditid')
            return func(id)
        super(WorkOrderApi, self).put()

        return self.render_json()

    def delete(self, id):
        super(TaskApi, self).delete()
        TaskModel.query.filter_by(id=id).delete()
        cron.remove_crontjob(id)

    def database(self):
        super(WorkOrderApi, self).get()
        db = Mymysql()
        success, db_list = db.execute_sql('show databases')
        db.close()
        if not success:
            return self.render_json(code=3000, message=db_list)
        db_sys = ['information_schema', 'mysql', 'performance_schema']
        data = []
        count = 1
        for database in db_list:
            if database[0] not in db_sys:
                data.append({'id': count, 'name': database[0]})
                count += 1
        return self.render_json(data=data)

    def check_sql(self, sql):
        Manipulation_list=['create','delete','update','alter','insert']
        flag = 1
        sql_list = sql.split(';')
        res = []
        for sql_line in sql_list:
            sql_line = sql_line.strip()
            sql_split = sql_line.split()
            if sql_line == '':
                continue
            if len(sql_split) < 2 :
                flag = 2
                break
            res.append(sql_line)
            Manipulation = sql_split[0]
            Resource = sql_split[1]
            if Manipulation.lower() not in Manipulation_list:
                flag = 2
                break
            if not (Manipulation.lower() == 'create'
                    and Resource.lower() == 'table'):
                flag = 3
                break

        if len(res) == 0:
            flag = 2
        return flag, res

    def batch_execute_sql(self, sql_list):
        db = Mymysql()
        for sql in sql_list:
            success, res = db.execute_sql(sql)
            if not success:
                raise BaseHttpException(code=3000, message=res)
        db.close()

    def audit(self, id):
        self.super_api=True
        super(WorkOrderApi,self).put()
        work = WorkOrderModel.query.filter_by(id=id).first()
        sql_list=work.sql.split(';')
        cron.add_sql_job(id,sql_list)
        WorkOrderModel.query.filter_by(id=id).update({'audit': 1})
        return self.render_json()
