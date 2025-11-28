from fastapi import FastAPI
from models.users import UsersOrm


class UserAdminView(ModelView, model = UsersOrm):
    can_create = True
    column_list = ('id', 'link', 'timestamp')
    form_columns = ('id', 'link', 'timestamp')


def setup_admin(app: FastAPI, engine):
    admin = Admin(app, engine, title='Admin panel')
    admin.add_view(UserAdminView)
