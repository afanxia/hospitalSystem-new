import datetime as dt
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from flask_login import AnonymousUserMixin, UserMixin
from .base import db, BaseModel, I18NModel

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)


role_perm = db.Table(
    'role_perm',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('perm_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
)


class Permission(BaseModel):
    id = db.Column(db.Integer(),
                   Sequence('permission_seq', start=1000, increment=1),
                   primary_key=True)
    menu_code = db.Column(db.String(64), nullable=False) # 归属菜单,前端判断并展示菜单使用
    menu_name = db.Column(db.String(64), nullable=False) # 菜单的中文释义
    code = db.Column(db.String(64), unique=True, nullable=False) # 权限的代码/通配符,对应代码中@resource_need_perms等的value
    name = db.Column(db.String(64), nullable=False) # 本权限的中文释义
    desc = db.Column(db.String(256))
    system = db.Column(db.Boolean)
    roles = relationship('Role', secondary=role_perm, back_populates='perms')


class Role(BaseModel):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    update_time = db.Column(db.DateTime)
    desc = db.Column(db.String(256))
    perms = relationship('Permission', secondary=role_perm, back_populates='roles')
    users = relationship('User', secondary=user_role, back_populates='roles')

    def has_permission(self, perm):
        return any((x.name == perm for x in self.perms))


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    nickname = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    update_time = db.Column(db.DateTime)
    phone = db.Column(db.String(32))
    disabled = db.Column(db.Boolean(), default=False, nullable=False)
    roles = relationship('Role', secondary=user_role, back_populates='users')

    def populate(self, json_data):
        for k, v in json_data.items():
            if k == 'password':
                self.set_password(v)
            else:
                setattr(self, k, v)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def generate_confirmation_token(self, expiration=3600):
        """生成token"""
        s = Serializer(current_app.config["SECRET_KEY"], expiration)

        # 把 id、username、roles 放进 token
        token = s.dumps({
            "id": self.id,
            "username": self.username,
            "roles": [role.name for role in self.roles]
        }).decode()
        return token

    @staticmethod
    def confirm(token):
        """验证token"""
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None

        return data

    @property
    def is_root(self):
        return self.is_authenticated and self.username == 'root'

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def has_role(self, role):
        return self.is_root or any([x.name == role for x in self.roles])

    def has_permission(self, perm):
        return self.is_root or any(
            (x.has_permission(perm) for x in self.roles)
        )

    def has_perms(self, perms):
        if self.is_root:
            return True
        myperms = []
        for x in self.roles:
            myperms.extend(x.perms)
        myperms = [x.name for x in myperms]
        return set(perms).issubset(myperms)

    def __repr__(self):
        return '<User %r>' % self.username

    def _asdict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns
                if c.name != 'password'}


root = User(id='0', username='root', password='Iwntellyou!!!')
