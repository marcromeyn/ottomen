from . import ProjectApiTestCase
from ..factories import AccountFactory
from ottomen.resources import services


class AccountApiTestCase(ProjectApiTestCase):
    def test_test(self):
        r = self.send_get_request('/session/test')
        self.assertOkJson(r)