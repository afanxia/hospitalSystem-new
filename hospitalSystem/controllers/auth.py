from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user as tusr

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.perm import perms_required, resource_need_perms
from hospitalSystem.const import (PMS_CONFIG_USER, PMS_CONFIG_ROLE, PMS_ATTACH_ROLE,
                           PMS_CONFIG_PERMISSION)
#from .base import register_api, Resource, I18NResource
#from .base import register_api, BaseResource, I18NResource
from flask_restplus import Resource

from hospitalSystem.utils.dto import AuthDto

auth_api = AuthDto.api
user_auth = AuthDto.user_auth

@auth_api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @auth_api.doc('user login')
    @auth_api.expect(user_auth, validate=True)
    def post(self):
        data = request.get_json()
        if data['username'] == 'root':
            user = root
        else:
            user = User.query.filter_by(username=data['username']).first()

        if not user:
            err_msg = _('User not existed.')
            raise Error(err_msg, 404)

        if user.disabled:
            err_msg = _('user was disabled, cannot login')
            raise Error(err_msg, 400)

        if user.check_password(data['password']):
            login_user(user)
            return jsonify(user)
        else:
            err_msg = _('password error')
            raise Error(err_msg, 400)


@auth_api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @auth_api.doc('logout a user')
    def delete(self):
        logout_user()
        return jsonify({'err': 0})

