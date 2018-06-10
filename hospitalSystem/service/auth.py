from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user as tusr

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.status import confirm_token, confirm_key, Status
from hospitalSystem.utils.gravatar import gravatar

class AuthService:

    @staticmethod
    def login(data):
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
            ret_json = {
                "status": Status.SUCCESS.status,
                "message": "login success!",
                "request": request.base_url,
                "data": {
                    "token": "",
                }
            }
            token = user.generate_confirmation_token()
            ret_json.update({"data": {"token": token}})
            return jsonify(ret_json)
            #return jsonify(user)
        else:
            err_msg = _('password error')
            raise Error(err_msg, 400)

    @staticmethod
    def logout():
        logout_user()
        ret_json = {
            "status": Status.SUCCESS.status,
            "message": "logout!",
            "request": request.base_url,
            "data": {}
        }
        return jsonify(ret_json)

    @staticmethod
    def get_logged_in_user_info():
        token = request.values.get("token")
        confirm_data = User.confirm(token)
        uid = confirm_data['id']
        user = User.query.filter_by(id=uid).first()
        role = user.roles[0]
        permissions = role.perms
        menuList = list(set(perm.menu_code for perm in permissions))
        permissionList = [perm.code for perm in permissions]

        ret_json = {
            "status": Status.SUCCESS.status,
            "message": Status.SUCCESS.message,
            "request": request.base_url,
            "userPermission": {
                "userId": user.id,
                "roleId": role.id,
                "nickname": user.nickname,
                "avatar": gravatar(user.username),
                "roleName": role.name,
                "menuList": menuList,
                "permissionList": permissionList
            }
        }
        return jsonify(ret_json)
