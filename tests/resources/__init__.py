from .. import OttomenAppTestCase, settings


class OttomenResourceTestCase(OttomenAppTestCase):
    def setUp(self):
        super(OttomenResourceTestCase, self).setUp()
        # self.token = self._login()

class OttomenResourceTestCaseWithPopulatedDb(OttomenAppTestCase):
    def setUp(self):
        super(OttomenResourceTestCaseWithPopulatedDb, self).setUp()

    @classmethod
    def setUpClass(cls):
        super(OttomenResourceTestCaseWithPopulatedDb, cls).setUpClass()
        cls._create_fixtures()