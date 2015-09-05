import click
from werkzeug.datastructures import MultiDict

from ..resources.services import accounts as service
from ..helpers import encrypt_password


@click.group()
def accounts():
    pass


@accounts.command(name='create')
def account_create():
    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True)
    password_confirm = click.prompt('Confirm Password', hide_input=True)
    data = MultiDict(dict(email=email, password=password, password_confirm=password_confirm))

    return data


@accounts.command(name='delete')
def account_delete():
    email = click.prompt('Email')
    user = service.first(email=email)
    if not user:
        print('Invalid user')
        return
    service.delete(user)
    print('User deleted successfully')


@accounts.command(name='list')
def account_list():
    for u in service.all():
        print('User(id=%s email=%s)' % (u.id, u.email))
