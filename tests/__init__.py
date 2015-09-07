from unittest import TestCase
import pytest

from .utils import FlaskTestCaseMixin


class ProjectTestCase(TestCase):
    pass


@pytest.mark.usefixtures("app", "db", "session")
class ProjectAppTestCase(FlaskTestCaseMixin, ProjectTestCase):
    def setUp(self):
        super(ProjectAppTestCase, self).setUp()

    def tearDown(self):
        super(ProjectAppTestCase, self).tearDown()


    # def _login(self, username=None, password=None):
    #     username = username or self.account.username
    #     password = password or 'password'
    #     data = self.jpost('/auth', data={'username': username, 'password': password}, follow_redirects=False)
    #     return json.loads(data.data.decode())
