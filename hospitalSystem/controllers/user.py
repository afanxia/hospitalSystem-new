from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user as tusr

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.perm import perms_required, resource_need_perms
from hospitalSystem.const import (PMS_ADD_USER, PMS_UPDATE_USER, PMS_DELETE_USER)
#from .base import register_api, Resource, I18NResource
from .base import register_api, BaseResource, I18NResource
from flask_restplus import Resource
from hospitalSystem.service.user import UserService
from hospitalSystem.utils.dto import UserDto

user_api = UserDto.api
_user = UserDto.user


@resource_need_perms('POST', PMS_ADD_USER)
@user_api.route('/')
class UserListView(BaseResource):
    model = User

    @user_api.doc('list_of_registered_users')
    @user_api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return super().get(None)

    @user_api.expect(_user, validate=True)
    @user_api.doc('create new user(s)')
    def post(self):
        """Creates new User(s) """
        return super().post()


@resource_need_perms('POST', PMS_ADD_USER)
@resource_need_perms('PATCH', PMS_UPDATE_USER)
@resource_need_perms('DELETE', PMS_DELETE_USER)
@user_api.param('uid', 'The User identifier')
@user_api.route('/<int:uid>')
#@user_api.response(404, 'User not found.')
class UserView(BaseResource):
    model = User

    @user_api.doc('get a user')
    @user_api.marshal_with(_user)
    def get(self, uid):
        return super().get(uid)

    @user_api.expect(_user, validate=True)
    @user_api.doc('create a new user')
    def post(self):
        return super().post()

    @user_api.expect(_user, validate=True)
    @user_api.doc('patch a user')
    def patch(self, uid):
        return super().patch(uid)

    @user_api.doc('delete a user')
    def delete(self, uid):
        return super().delete(uid)


@user_api.param('uid', 'The User identifier')
@user_api.route('/<int:uid>/uroles')
class UserRolesList(Resource):
    @user_api.doc('List all roles for a user')
    def get(self, uid):
        return UserService.get_user_roles(uid)


@user_api.param('uid', 'The User identifier')
@user_api.param('rid', 'The Role identifier')
@user_api.route('/<int:uid>/uroles/<int:rid>')
class UserRoles(Resource):
    @user_api.doc('add a role for a user')
    @perms_required(PMS_UPDATE_USER)
    def post(self, uid, rid):
        return UserService.add_user_role_by_id(uid, rid)

    @user_api.doc('delete a permission for a user')
    @perms_required(PMS_UPDATE_USER)
    def delete(self, uid, rid):
        return UserService.delete_user_role_by_id(uid, rid)
