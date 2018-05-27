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

from hospitalSystem.utils.dto import RoleDto

role_api = RoleDto.api
_role = RoleDto.role


@resource_need_perms('POST', PMS_CONFIG_ROLE)
@role_api.route('/')
class RoleListView(BaseResource):
    model = Role

    @role_api.doc('list_of_roles')
    @role_api.marshal_list_with(_role, envelope='data')
    def get(self):
        """List all roles"""
        return super().get(None)

    @role_api.expect(_role, validate=True)
    @role_api.doc('create new role(s)')
    def post(self):
        """Creates new Role(s) """
        return super().post()


@resource_need_perms('POST', PMS_CONFIG_ROLE)
@resource_need_perms('PATCH', PMS_CONFIG_ROLE)
@resource_need_perms('DELETE', PMS_CONFIG_ROLE)
@role_api.param('rid', 'The Role identifier')
@role_api.route('/<int:rid>')
#@role_api.response(404, 'Role not found.')
class RoleView(BaseResource):
    model = Role

    @role_api.doc('get a role')
    @role_api.marshal_with(_role)
    def get(self, rid):
        return super().get(rid)

    @role_api.expect(_role, validate=True)
    @role_api.doc('create a new role')
    def post(self):
        return super().post()

    @role_api.expect(_role, validate=True)
    @role_api.doc('patch a role')
    def patch(self, rid):
        return super().patch(rid)

    @role_api.doc('delete a role')
    def delete(self, rid):
        return super().delete(rid)


@role_api.param('rid', 'The Role identifier')
@role_api.route('/<int:rid>/perms')
class RolePermissionsList(Resource):
    @role_api.doc('List all permissions for a role')
    def get(self, rid):
        role = Role.query.filter(Role.id == rid).one()
        return jsonify(role.perms)


@role_api.param('rid', 'The Role identifier')
@role_api.param('pid', 'The Permission identifier')
@role_api.route('/<int:rid>/perms/<int:pid>')
class RolePermissions(Resource):
    @role_api.doc('add a permission for a role')
    @perms_required(PMS_CONFIG_ROLE)
    def post(self, rid, pid):
        ins = role_perm.insert().values(role_id=rid, perm_id=pid)
        db.session.execute(ins)
        db.session.commit()
        return jsonify(ok_rt)

    @role_api.doc('delete a permission for a role')
    @perms_required(PMS_CONFIG_ROLE)
    def delete(self, rid, pid):
        st = role_perm.delete().where(
            and_(role_perm.c.role_id == rid, role_perm.c.perm_id == pid))
        db.session.execute(st)
        db.session.commit()
        return jsonify(ok_rt)

