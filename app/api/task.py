from . import SecurityResource
from app.model.business import BusinessModel, PermissionModel
from apscheduler.triggers.cron import CronTrigger
from app.model.task import TaskModel
from app.model.user import UserModel
from flask_login import login_required, current_user
from app.form.task import TaskForm
from flask import request
from app.lib.extensions import cron


class TaskApi(SecurityResource):
    column = ['business_id', 'schedule', 'shell', 'comment']
    module = 'task'

    def get_tasks(self):
        task_id_list = []
        if current_user.is_super():
            tasks = TaskModel.query.all()
            for task in tasks:
                task_id_list.append(task.id)
            return task_id_list
        query = BusinessModel.query.filter_by(user_id=current_user.id).all()
        # query = UserModel
        for business in query:
            for task in business.task:
                task_id_list.append(task.id)
        return task_id_list

    def get(self, id=None):
        if id:
            task = TaskModel.query.filter_by(id=id).first().to_json()
            return self.render_json(data=task)

        super(TaskApi, self).get()
        task_list = []
        if current_user.is_super():
            tasks = TaskModel.query.all()
            for task in tasks:
                task_list.append(task.to_json())
            return TaskApi.render_json(data=task_list)

        query = UserModel.query.filter_by(id=current_user.id).first().business
        for business in query:
            for task in business.task:
                task_list.append(task.to_json())
        return self.render_json(data=task_list)

    def post(self):
        super(TaskApi, self).post()
        form = TaskForm(request.form, csrf=False)
        schedule = form.schedule.data
        try:
            CronTrigger.from_crontab(schedule)
        except:
            return self.render_json(code=4000)
        shell = form.shell.data
        comment = form.comment.data
        business_id = form.business_id.data
        ip = BusinessModel.query.filter_by(id=business_id).first().host
        value_list = [business_id, schedule, shell, comment]
        taskinfo = dict(zip(self.column, value_list))
        task = TaskModel(**taskinfo)
        task.save()
        cron.add_cronjob(schedule, shell, str(task.id), ip)
        info =  '周期:' + schedule + ' 命令:' + shell
        self.log(info=info)
        return self.render_json()

    def put(self, id):
        super(TaskApi, self).put()
        form = TaskForm(request.form, csrf=False)
        schedule = form.schedule.data
        try:
            CronTrigger.from_crontab(schedule)
        except:
            return self.render_json(code=4000)
        shell = form.shell.data
        comment = form.comment.data
        business_id = form.business_id.data
        ip = BusinessModel.query.filter_by(id=business_id).first().host
        value_list = [business_id, schedule, shell, comment]
        taskinfo = dict(zip(self.column, value_list))
        task = TaskModel.query.filter_by(id=id).first()
        before_list = [task.business_id, task.schedule, task.shell, task.comment]
        if value_list == before_list:
            print('无需更新')
            return self.render_json()
        before = '任务id:' + str(id) + ' 周期:' + task.schedule + ' 命令:' + task.shell
        after = '任务id:' + str(id) + ' 周期:' + schedule + ' 命令:' + shell
        TaskModel.query.filter_by(id=id).update(taskinfo)
        cron.remove_crontjob(id)
        cron.add_cronjob(schedule, shell, str(id), ip)
        self.log(before=before, after=after)
        return self.render_json()

    def delete(self, id):
        super(TaskApi, self).delete()
        task=TaskModel.query.filter_by(id=id).first()
        info = '任务id:' + str(id) + ' 周期:' + task.schedule + ' 命令:' + task.shell
        TaskModel.query.filter_by(id=id).delete()
        cron.remove_crontjob(id)
        self.log(info=info)

