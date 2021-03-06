import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from app import create_app
from app.models.base import db
from app.models.user import User
from click import confirm

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server(host="127.0.0.1", port=5000))
manager.add_command("db", MigrateCommand)  # 数据库管理
manager.add_command("clean", Clean())  # 清理缓存文件
manager.add_command("url", ShowUrls())  # 打印所有URL


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def db_create_first():
    ret = confirm("drop the database?")
    if ret:
        db.drop_all()
        print("drop finish!")
    db.create_all()
    print("The database is created successfully!")
    create_supper_user()


def create_role(name='admin'):
    from app.models.role import Role
    admin = Role.query.filter_by(name=name).first()
    if not admin:
        with db.auto_commit():
            admin = Role()
            admin.name = name
            db.session.add(admin)
            print("The '%s' role is created!" % name)
    return admin


@manager.command
def create_supper_user():
    admin = create_role()
    username = input('Please Enter the superuser username:')
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
    holder = input("Holder")
    with db.auto_commit():
        user = User()
        user.username = username
        user.password = password
        user.holder = holder
        user.roles = [admin]
        db.session.add(user)
        print("Superuser is created successfully!")
    create_role_hr()


def create_role_hr():
    from app.models.role import Role
    with db.auto_commit():
        leader_role = Role()
        leader_role.name = 'hr'
        db.session.add(leader_role)


@manager.command
def test():
    """run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
