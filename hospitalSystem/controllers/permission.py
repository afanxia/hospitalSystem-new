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
from .base import register_api, BaseResource, I18NResource
from flask_restplus import Resource

from hospitalSystem.utils.dto import PermissionDto

perm_api = PermissionDto.api
_perm = PermissionDto.permission


@resource_need_perms('POST', PMS_CONFIG_PERMISSION)
@perm_api.route('/')
class PermissionListView(BaseResource):
    model = Permission

    @perm_api.doc('list_of_permissions')
    @perm_api.marshal_list_with(_perm, envelope='data')
    def get(self):
        """List all permissions"""
        return super().get(None)

    @perm_api.expect(_perm, validate=True)
    @perm_api.doc('create new permission(s)')
    def post(self):
        """Creates new Permission(s) """
        return super().post()


@resource_need_perms('POST', PMS_CONFIG_PERMISSION)
@resource_need_perms('PATCH', PMS_CONFIG_PERMISSION)
@resource_need_perms('DELETE', PMS_CONFIG_PERMISSION)
@perm_api.param('rid', 'The Permission identifier')
@perm_api.route('/<int:rid>')
#@perm_api.response(404, 'Permission not found.')
#class PermissionView(I18NResource):
class PermissionView(BaseResource):
    model = Permission

    @perm_api.doc('get a permission')
    @perm_api.marshal_with(_perm)
    def get(self, rid):
        return super().get(rid)

    @perm_api.expect(_perm, validate=True)
    @perm_api.doc('create a new permission')
    def post(self):
        return super().post()

    @perm_api.expect(_perm, validate=True)
    @perm_api.doc('patch a permission')
    def patch(self, rid):
        perm = Permission.query.filter_by(id=rid).one()
        if perm.system:
            raise Error('system permission is not editable', 401)
        return super().patch(rid)

    @perm_api.doc('delete a permission')
    def delete(self, rid):
        perm = Permission.query.filter_by(id=rid).one()
        if perm.system:
            raise Error('ask your admin for support', 401)
        return super().delete(rid)

