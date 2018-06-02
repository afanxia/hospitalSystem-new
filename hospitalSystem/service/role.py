from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user as tusr

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.status import confirm_token, confirm_key, Status


class RoleService:

    @staticmethod
    def get_role_permissions(rid):
        role = Role.query.filter(Role.id == rid).one()
        return jsonify(role.perms)

    @staticmethod
    def add_role_permission_by_id(rid, pid):
        ins = role_perm.insert().values(role_id=rid, perm_id=pid)
        db.session.execute(ins)
        db.session.commit()
        return jsonify(ok_rt)

    @staticmethod
    def delete_role_permission_by_id(rid, pid):
        st = role_perm.delete().where(and_(role_perm.c.role_id == rid, role_perm.c.perm_id == pid))
        db.session.execute(st)
        db.session.commit()
        return jsonify(ok_rt)
