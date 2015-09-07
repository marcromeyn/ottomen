import pytest
from ottomen.web.api import create_app
from ottomen.core import db
from .populate_db import populate_db
from . import settings


# @pytest.fixture(scope='class')
# def app(request):
#     app = create_app(settings)
#
#     # Establish an application context before running the tests.
#     ctx = app.app_context()
#     ctx.push()
#
#     def teardown():
#         ctx.pop()
#
#     request.addfinalizer(teardown)
#     request.cls.app = app
#     request.cls.ctx = ctx
#
#     return app
#
#
# @pytest.fixture(scope='class')
# def db(app, request):
#     """Session-wide test database."""
#
#     def teardown():
#         _db.drop_all()
#
#     _db.init_app(app)
#     _db.create_all()
#     # _db.engine.raw_connection().connection.text_factory = str
#
#     connection = _db.engine.connect()
#     options = dict(bind=connection)
#     populate_db(_db.session)
#
#     request.addfinalizer(teardown)
#     request.cls.db = _db
#     return _db


# @pytest.fixture(scope='function')
# def session(request):
#     """Creates a new database session for a test."""
#     connection = db.engine.connect()
#     transaction = connection.begin()
#
#     options = dict(bind=connection, binds={})
#     session = db.create_scoped_session(options=options)
#
#     db.session = session
#
#     def teardown():
#         transaction.rollback()
#         connection.close()
#         session.remove()
#
#     request.addfinalizer(teardown)
#     return session
