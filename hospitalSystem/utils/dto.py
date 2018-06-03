from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('users', description='user related operations')
    user = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'phone': fields.Integer(required=True, description='user telephone number'),
        'disabled': fields.Boolean(description='disabled or not'),
        'nickname': fields.String(required=True, description='user nickname'),
    })

class RoleDto:
    api = Namespace('roles', description='role related operations')
    role = api.model('role', {
        'name': fields.String(required=True, description='role name'),
        'desc': fields.String(required=True, description='role description'),
    })

class PermissionDto:
    api = Namespace('permissions', description='permission related operations')
    permission = api.model('permission', {
        'name': fields.String(required=True, description='permission name'),
        'desc': fields.String(required=True, description='permission description'),
        'display': fields.String(required=True, description='display info'),
        'system': fields.Boolean(description='is system permission or not'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='The user password '),
    })
