from unittest import TestCase
import pytest
from .populate_db import populate_db
from ottomen.core import db

from ottomen.web.api import create_app
from .utils import FlaskTestCaseMixin
from . import settings


class OttomenTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


class OttomenAppTestCase(FlaskTestCaseMixin, OttomenTestCase):
    # def setUp(self):
    #     super(ProjectAppTestCase, self).setUp()
    #
    # def tearDown(self):
    #     super(ProjectAppTestCase, self).tearDown()

    @classmethod
    def _create_app(self):
        return create_app(settings, register_security_blueprint=True)

    @classmethod
    def _create_fixtures(cls):
        # self.account = AccountFactory()
        # services.accounts.save(self.account)
        db.drop_all()
        db.create_all()
        populate_db(db.session)

    @classmethod
    def setUpClass(cls):
        super(OttomenAppTestCase, cls).setUpClass()
        cls.app = cls._create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        super(OttomenAppTestCase, cls).tearDownClass()
        db.session.commit()
        db.drop_all()
        cls.app_context.pop()

    def db_session(self):
        session = db.create_scoped_session()

        return session

    # def _login(self, username=None, password=None):
    #     username = username or self.account.username
    #     password = password or 'password'
    #     data = self.jpost('/auth', data={'username': username, 'password': password}, follow_redirects=False)
    #     return json.loads(data.data.decode())
