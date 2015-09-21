import click
from werkzeug.serving import run_simple
from ottomen.web import application
from ottomen import settings
from ottomen.manage.database import database
from ottomen.manage.accounts import accounts

from ottomen.web.api import create_app
from ottomen.core import db, mem
from ottomen.algorithm.experiment import *
from ottomen.algorithm import globals
from ottomen.algorithm.worker import *
from tests import populate_db

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
    

@cli.command()
def seed():
    db.drop_all()
    db.create_all()
    mem.flushdb()
    populate_db(db.session)
    set_sizes = 500
    set_limit = 200
    worker_id = 'turkleton'
    exp = new_experiment(1337, 0.98, set_limit=set_limit, set_sizes=set_sizes)
    db_worker = workers.save(Worker(id=worker_id))
    task = new_task('1337',     1337)
    worker = workers.new_mem(1337, db_worker)
    validated_qs_batch = 25
    session_id = 'gaysession'

if __name__ == '__main__':
    cli()
