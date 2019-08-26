from . import SecurityResource
from app.model.user import UserModel
from app.model.sidebar import SideBarModel
from flask_login import login_required, current_user
from flask import request


class SideBarApi(SecurityResource):

    def get(self):
        super(SideBarApi, self).get()
        if current_user.is_super():
            super_sidebar_list = []
            super_sidebars = SideBarModel.query.all()
            for side in super_sidebars:
                super_sidebar_list.append(side.to_json())
            return self.render_json(data=super_sidebar_list)
        common_sidebar_list = []
        common_sidebars = SideBarModel.query.filter_by(is_super=0).all()
        for side in common_sidebars:
            common_sidebar_list.append(side.to_json())
        return self.render_json(data=common_sidebar_list)
