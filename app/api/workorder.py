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
    column = ['name', 'sql', 'comment']

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
        form = WorkOrderForm(request.form, csrf=False)
        name = form.name.data
        sql = form.sql.data
        comment = form.comment.data
        value_list = [name, sql, comment]
        workinfo = dict(zip(self.column, value_list))
        workinfo['type'] = 1
        flag, res = self.check_sql(sql)
        if flag == 1:
            # 自动审核
            workinfo['audit'] = 2
            workinfo['finish'] = 1
            self.batch_execute_sql(res)
            workinfo['result'] = 'success'
        elif flag == 2:
            return self.render_json(code=3000, message='sql不合法')
        elif flag == 3:
            # 人工审核
            pass
        elif flag == 4:
            return self.render_json(code=3000, message='请删除注释行')
        else:
            return self.render_json(code=9999, message='未知错误')
        workinfo['sql'] = ';\n'.join(res)
        workinfo['user_id'] = current_user.id
        work = WorkOrderModel(**workinfo)
        work.save()
        return self.render_json()

    def put(self, tag=None):
        if tag:
            func = getattr(self, tag, 'audit')
            return func()
        super(WorkOrderApi, self).put()

        return self.render_json()

    def delete(self, id):
        super(TaskApi, self).delete()
        TaskModel.query.filter_by(id=id).delete()
        cron.remove_crontjob(id)

    def database(self):
        super(WorkOrderApi, self).get()
        db = Mymysql()
        success, db_list = db.execute_one_sql('show databases')
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
        Manipulation_list = ['create', 'delete', 'update', 'alter', 'insert']
        flag = 1
        sql_list = sql.split(';')
        res = []
        for sql_line in sql_list:
            sql_line = sql_line.strip()
            if sql_line.startswith('#'):
                flag = 4
                break
            if sql_line.startswith('/'):
                flag = 4
                break
            if sql_line.startswith('--'):
                flag = 4
                break
            sql_split = sql_line.split()
            if sql_line == '':
                continue

            if len(sql_split) < 2:
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

        if len(res) == 0:
            flag = 2
        return flag, res

    def batch_execute_sql(self, sql_list):
        db = Mymysql()
        for sql in sql_list:
            success, res = db.execute_one_sql(sql)
            if not success:
                raise BaseHttpException(code=3000, message=res)
        db.close()

    def audit(self):
        self.super_api = True
        super(WorkOrderApi, self).put()
        id = request.form.get('id')
        work = WorkOrderModel.query.filter_by(id=id).first()
        sql_list = work.sql.split(';')
        cron.add_sql_job(id, sql_list)
        WorkOrderModel.query.filter_by(id=id).update({'audit': 1})
        return self.render_json()

    def execute(self):
        id = request.form.get('id')
        self.super_api = True
        super(WorkOrderApi, self).put()
        work = WorkOrderModel.query.filter_by(id=id).first()
        if work.finish == 1:
            return self.render_json(message='无法重复执行')
        sql_list = work.sql.split(';')
        cron.add_sql_job(id, sql_list)
        return self.render_json(message='后台执行中,若未完成请稍后刷新页面')

    def item(self):
        id = request.args['id']
        work = WorkOrderModel.query.filter_by(id=id).first()
        data = work.to_json()
        return self.render_json(data=data)

    def edit(self):
        id = request.form.get('id')
        work = WorkOrderModel.query.filter_by(id=id).first()
        sql = request.form.get('sql')
        flag, res = self.check_sql(sql)
        if flag == 2:
            return self.render_json(code=3000, message='sql不合法')
        if flag == 4:
            return self.render_json(code=3000, message='请删除注释')

        for col in self.column:
            setattr(work, col, request.form.get(col))
        work.audit = 0
        work.save()
        return self.render_json()
