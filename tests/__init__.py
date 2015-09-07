from unittest import TestCase
import pytest
from .populate_db import populate_db
from ottomen.core import db

from ottomen.web.api import create_app
from .utils import FlaskTestCaseMixin
from . import settings


class OttomenTestCase(TestCase):
    pass


class OttomenAppTestCase(FlaskTestCaseMixin, OttomenTestCase):
    # def setUp(self):
    #     super(ProjectAppTestCase, self).setUp()
    #
    # def tearDown(self):
    #     super(ProjectAppTestCase, self).tearDown()

    def _create_app(self):
        return create_app(settings, register_security_blueprint=True)

    def _create_fixtures(self):
        # self.account = AccountFactory()
        # services.accounts.save(self.account)
        populate_db(db.session)

    def setUp(self):
        super(OttomenAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self._create_fixtures()

    def tearDown(self):
        super(OttomenAppTestCase, self).tearDown()
        db.session.commit()
        db.drop_all()
        self.app_context.pop()

    def db_session(self):
        session = db.create_scoped_session()

        return session

    # def _login(self, username=None, password=None):
    #     username = username or self.account.username
    #     password = password or 'password'
    #     data = self.jpost('/auth', data={'username': username, 'password': password}, follow_redirects=False)
    #     return json.loads(data.data.decode())
