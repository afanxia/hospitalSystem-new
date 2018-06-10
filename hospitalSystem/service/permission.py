from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user as tusr

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.status import confirm_token, confirm_key, Status


class PermissionService:

    @staticmethod
    def listPermissionPage():
        tmpList = []
        perms = Permission.query.all()
        menuCodeSet = set(perm.menu_code for perm in perms)
        for menuCode in menuCodeSet:
            menuName = ''
            tmpPerms = []
            tmpMenu = {}
            for perm in perms:
                if perm.menu_code == menuCode:
                    menuName = perm.menu_name
                    tmpPerms.append(perm)
            tmpMenu.update(
                {
                    "menuName": menuName,
                    "permissions": tmpPerms,
                }
            )
            tmpList.append(tmpMenu)

        ret_json = {
            "status": Status.SUCCESS.status,
            "message": Status.SUCCESS.message,
            "request": request.base_url,
            "list": tmpList
        }
        return jsonify(ret_json)