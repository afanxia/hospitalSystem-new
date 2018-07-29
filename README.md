## Inspiration
This project is inspired by [SpringBoot-Shiro-Vue](https://github.com/Heeexy/SpringBoot-Shiro-Vue), which is a SpringBoot(Java) practice. Many thanks to the author.
In this project, I've been trying to implement the backend with Python, with a consistent permission controlling method in the original one, i.e., RBAC(role based access control).

It is also a chance for me to play with Python/Flask, and could be a boilerplate to build a Python webapp.

## Get start
**!! Using `python3.6` or later version.**
```bash
$> git clone [this project]
$> # replace appname with your application name
$> make rename
```

## Commands
There are 2 scripts in this project directory. `Makefile` and `manage.py`.
Open your terminal to check its capabilities.
```bash
make
```
or
```
python manage.py
```
## Create Database
```
python manage.py create_db
```

## Database Migration

```bash
$ # do it only if no `migrations` folder under your project folder
$ python manage.py db init
$ # do it every time before submitting changes of models
$ python manage.py db migrate
$ # do it so database is upgraded with your changes of models
$ python manage.py db upgrade
$ python manage.py db --help
```

## Configuration & Environment
```bash
$ export SQLALCHEMY_DATABASE_URI='mysql+pymysql://[usr:pwd]@localhost:32768/enmon?charset=utf8'
$ # [usr:pwd] are placehoder of database user and password
```

## Localization
```bash
$ python manage.py babel
$ update
$ # edit translations/zh/messages.po, then
$ python manage.py babel
$ compile
```

## RBAC page
![RBAC](http://ots7yt7am.bkt.clouddn.com/blog/role_permission.png)