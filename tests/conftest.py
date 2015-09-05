import os
import pytest

from ottomen.factory import create_app
from ottomen.core import db as _db
from ottomen.resources.models import Experiment, Question, Label, Validation
import datetime
import csv

TEST_DATABASE_URI = 'postgres://postgres:turkturk@localhost:5432/mturk_test'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    settings_override = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.init_app(app)
    _db.create_all()
    _db.engine.raw_connection().connection.text_factory = str

    connection = _db.engine.connect()
    options = dict(bind=connection)
    populate_db(_db.create_session(options))

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


def populate_db(session):
    print 'starting db populate....'
    # experiments
    with open('experiment.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            exp = Experiment(**row)
            exp.id = int(row['id'])
            exp.completed = row['completed'] == 't'
            exp.end_date = None
            session.add(exp)

    # questions
    with open('question.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            q = Question(**row)
            q.id = int(row['id'])
            q.in_progress = row['in_progress'] == 't'
            q.belief = row['belief'] == 't'
            session.add(q)

    malwares = {}
    # malware
    with open('malware.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            mw = Label(**row)
            mw.id = int(row['id'])
            mw.timestamp = datetime.datetime.now()
            malwares[row['id']] = mw
            session.add(mw)


    validations = {}
    # validations
    with open('validation.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            val = Validation(**row)
            val.label = row['malware'] == 't'
            val.timestamp = datetime.datetime.now()
            validations[row['id']] = val
            session.add(val)

    # validation_malwares
    with open('validation_malware.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            validations[row['validation_id']].labels.append(malwares[row['malware_id']])

    session.commit()
    print 'complete'



