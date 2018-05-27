#!/usr/bin/env python

import os

from flask_script import Manager, Server, prompt_choices
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand
from hospitalSystem import create_app
from hospitalSystem.warmup import setup_db, update_perms, createsuperuser
from hospitalSystem.models import db, User
from hospitalSystem.settings import config_by_name


# default to dev config because no one should use this in
# production anyway
app = create_app(config_by_name[(os.getenv('BOILERPLATE_ENV') or 'dev')])
manager = Manager(app)


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, User=User)


@manager.command
def create_db():
    '''
        create database and tables
    '''
    setup_db(app, db)


@manager.command
def babel():
    """ to setup a new language translation.
        `pybabel init -i ./babel/messages.pot -d hospitalSystem/translations -l zh`
    """
    choices = (
        ("update", "extract text"),
        ("compile", "compile the translations")
    )

    op = prompt_choices("operation", choices=choices, resolve=str,
                        default="update")
    if op == 'update':
        os.system(
            'pybabel extract -F ./babel/babel.cfg -k lazy_gettext '
            '-o ./babel/messages.pot hospitalSystem'
        )
        os.system(
            'pybabel update -i ./babel/messages.pot -d hospitalSystem/translations'
        )
    elif op == 'compile':
        os.system('pybabel compile -d hospitalSystem/translations')


@manager.command
def create_admin():
    createsuperuser(db)


@manager.command
def update_db():
    update_perms(db)


if __name__ == "__main__":
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)
    manager.add_command("server", Server(host='0.0.0.0'))
    manager.add_command("show_urls", ShowUrls())
    manager.add_command("clean", Clean())
    manager.run()
