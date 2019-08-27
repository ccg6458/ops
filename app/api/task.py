from . import SecurityResource
from app.model.business import BusinessModel, PermissionModel
from app.model.task import TaskModel
from app.model.user import UserModel
from flask_login import login_required, current_user
from app.form.task import TaskForm
from flask import request
from app.lib.extensions import cron


class TaskApi(SecurityResource):
    cloumn = ['business_id', 'schedule', 'shell', 'comment']
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
        print(cron.sched.get_jobs())
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
        shell = form.shell.data
        comment = form.comment.data
        business_id = form.business_id.data
        ip = BusinessModel.query.filter_by(id=business_id).first().host
        value_list = [business_id, schedule, shell, comment]
        taskinfo = dict(zip(self.cloumn, value_list))
        task = TaskModel(**taskinfo)
        task.save()
        cron.add_cronjob(schedule, shell, str(task.id), ip)
        self.log(name=shell)
        return self.render_json()

    def put(self, id):
        super(TaskApi, self).post()
        form = TaskForm(request.form, csrf=False)
        schedule = form.schedule.data
        shell = form.shell.data
        comment = form.comment.data
        business_id = form.business_id.data
        ip = BusinessModel.query.filter_by(id=business_id).first().host
        value_list = [business_id, schedule, shell, comment]
        taskinfo = dict(zip(self.cloumn, value_list))
        TaskModel.query.filter_by(id=id).update(taskinfo)
        cron.remove_crontjob(id)
        cron.add_cronjob(schedule, shell, str(id), ip)
        return self.render_json()

    def delete(self, id):
        super(TaskApi, self).delete()
        TaskModel.query.filter_by(id=id).delete()
        cron.remove_crontjob(id)
