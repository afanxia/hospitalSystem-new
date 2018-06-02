from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.perm import perms_required, resource_need_perms
#from .base import register_api, Resource, I18NResource
from .base import register_api, BaseResource, I18NResource
from flask_restplus import Resource
from hospitalSystem.utils.status import confirm_token
from hospitalSystem.utils.dto import AuthDto
from hospitalSystem.service.auth import AuthService

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
        post_data = request.json
        return AuthService.login(data=post_data)


@auth_api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @auth_api.doc('logout a user')
    @confirm_token()
    def delete(self):
        return AuthService.logout()


@auth_api.route('/info')
class UserInfoAPI(Resource):
    """
    User Info Resource
    """
    @auth_api.doc('get current user info')
    @confirm_token()
    def get(self):
        return AuthService.get_logged_in_user_info()
