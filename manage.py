import click
from werkzeug.serving import run_simple
from ottomen.web import application
from ottomen import settings
from ottomen.manage.database import database
from ottomen.manage.accounts import accounts

from ottomen.web.api import create_app
from ottomen.core import db

app = create_app()
db.app = app


@click.group()
def cli():
    pass


cli.add_command(database)
cli.add_command(accounts)


@cli.command()
def runserver():
    "Starts the web server"
    run_simple('0.0.0.0', settings.PORT, application, use_reloader=settings.DEBUG, use_debugger=settings.DEBUG)


if __name__ == '__main__':
    cli()
