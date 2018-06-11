from sqlalchemy.sql import and_
from flask import Blueprint, request, jsonify
from flask_babel import gettext as _
from flask_login import login_user, logout_user, current_user as tusr

from hospitalSystem.models import db, User, Role, Permission, user_role, role_perm
from hospitalSystem.models.user import root
from hospitalSystem.error import Error, ok_rt
from hospitalSystem.utils.status import confirm_token, confirm_key, Status

from hospitalSystem.utils.fop import req_2_sql, get_fop


class UserService:

    @staticmethod
    def get_user_roles(uid):
        usr = User.query.filter(User.id == uid).one()
        return jsonify(usr.roles)

    @staticmethod
    def add_user_role_by_id(uid, rid):
        role = Role.query.filter_by(id=rid).one()
        perms = [x.name for x in role.perms]
        if not tusr.has_perms(perms):
            raise Error('permission disallowed', 401)
        ins = user_role.insert().values(user_id=uid, role_id=rid)
        db.session.execute(ins)
        db.session.commit()
        return jsonify(ok_rt)

    @staticmethod
    def delete_user_role_by_id(uid, rid):
        st = user_role.delete().where(and_(user_role.c.user_id == uid, user_role.c.role_id == rid))
        db.session.execute(st)
        db.session.commit()
        return jsonify(ok_rt)

    @staticmethod
    def listUserPage():
        filters, sorting, pagination = req_2_sql(request)
        q = ('select {selection} from {table} {filters} {sort} {pagination}')
        cnt = db.session.execute(q.format(
            table='user',
            selection='count(*)',
            filters=filters,
            sort=sorting,
            pagination=''
        )).scalar()

        filters, order_by, page, page_size = get_fop(request)
        pagination = User.query.order_by(User.id.desc()).paginate(page,per_page=page_size,error_out=False)
        users = pagination.items

        totalPage = 1
        if cnt > 0:
            totalPage = (cnt / page_size + 1) if (cnt % page_size > 0) else (cnt / page_size)

        # users = User.query.all()
        tmpList = []
        for user in users:
            tmpUser = {}
            tmpUser.update(
                {
                    "nickname": user.nickname,
                    "username": user.username,
                    "roleId": user.roles[0].id,
                    "roleName": user.roles[0].name,
                    "createTime": user.create_time,
                    "updateTime": user.update_time
                }
            )
            tmpList.append(tmpUser)

        ret_json = {
            "status": Status.SUCCESS.status,
            "message": Status.SUCCESS.message,
            "request": request.base_url,
            "totalCount": cnt,
            # "totalCount": len(tmpList),
            "totalPage": totalPage,
            "list": tmpList
        }
        return jsonify(ret_json)
