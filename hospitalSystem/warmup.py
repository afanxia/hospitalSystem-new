'''
数据库建好后，写入必要的基础数据
'''
import simplejson as json
from hospitalSystem.models import User, Role


def setup_db(app, sqla, database=None):
    db_uri, _ = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)
    db_name = _.split('?')[0]
    if database:
        db_name = database
    default_engine = sqla.create_engine(db_uri + '/mysql')
    conn = default_engine.connect()
    res = conn.execute('show databases')
    res = [x[0] for x in res]
    if db_name in res:
        print(db_name, 'database existed')
    else:
        conn.execute('commit')
        conn.execute('create database %s character set = utf8mb4' % db_name)
        conn.close()
        print(db_name, 'created')
    # create tables
    sqla.create_all()
    print('tables created')


def createrole(db, name="admin"):
    """创建Role"""
    # 查看 <name> 角色是否存在
    admin = Role.query.filter_by(name=name).first()
    # 如果没有，则创建角色
    if not admin:
        admin = Role()
        admin.name = name
        db.session.add(admin)
        db.session.commit()
        print("The '%s' role is created!" % name)
    return admin


def createsuperuser(db):
    """创建超级管理员"""

    admin = createrole(db)

    username = input("Please Enter the superuser username:")
    if not username:
        print("username is empty!")
        return

    if User.query.filter_by(username=username).first():
        print("There is the same superuser username!")
        return

    password = input("Password:")
    password2 = input("Confirm password:")
    if password != password2:
        print("password is not confirmed!")
        return

    admin = User(username=username, password=password)
    db.session.add(admin)
    db.session.commit()
    db.session.refresh(admin)

    print("Superuser is created successfully!")


def update_perms(db):
    with open('conf/permissions.json') as f:
        pmss = json.load(f)
        fmt = '({0[id]}, "{0[name]}", "{0[display]}", "{0[desc]}", 1)'
        pmss = [fmt.format(x) for x in pmss]
        db.session.execute('delete from `permission` where `id` < 0')
        q = ('insert into `permission`'
             ' (`id`, `name`, `display`, `desc`, `system`) values')
        q += ', '.join(pmss)
        db.session.execute(q)
        db.session.commit()
