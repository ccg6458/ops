from . import SecurityResource
from app.model.user import UserModel
from app.model.business import BusinessModel, PermissionModel
from flask_login import login_required, current_user
from collections import OrderedDict
import json

from flask import request


class BusinessApi(SecurityResource):
    def get(self, tag=None, id=None):
        if tag:
            func = getattr(self, tag, 'only_id')
            return func(id)
        super(BusinessApi, self).get()
        if current_user.is_super():
            query = BusinessModel.query.all()
        else:
            query = UserModel.query.filter_by(id=current_user.id).first().business
        business_list = []
        for data in query:
            business_list.append(data.to_json())
        return self.render_json(data=business_list)

    def post(self,id=None):
        id_list = request.form.to_dict()
        for business_id in id_list.values():
            PermissionModel(user_id=id,business_id=business_id).save()
        return self.render_json()

    def delete(self,id):
        user_id=id
        business_id=request.form.get('business_id')
        PermissionModel.query.filter_by(user_id=user_id,business_id=business_id).delete()


    def only_id(self, id):
        super(BusinessApi, self).get()
        business_list = []
        if current_user.is_super():
            query = BusinessModel.query.all()
        else:
            query = UserModel.query.filter_by(id=current_user.id).first().business
        for data in query:
            business_list.append({'id': data.id, 'name': data.name})
        return self.render_json(data=business_list)

    def business_grant(self, id):
        self.super_api = True
        super(BusinessApi, self).get()
        business_all = BusinessModel.query.all()
        business_user = UserModel.query.filter_by(id=id).first().business
        alread_id = []
        all_id = []
        already_list = []
        no_list = []

        for data in business_all:
            all_id.append(data.id)
        for data in business_user:
            already_list.append(data.to_id_name_json())
            alread_id.append(data.id)

        all_set = OrderedDict.fromkeys(all_id)
        for id in alread_id:
            del all_set[id]
        # 得到去重后business id列表
        res_id = all_set.keys()
        business_res = [BusinessModel.query.filter_by(id=id).first() for id in res_id]
        for data in business_res:
            no_list.append(data.to_id_name_json())

        data = {'already': already_list,
                'no': no_list}
        return self.render_json(data=data)
