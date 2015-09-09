from .. import OttomenAppTestCase, settings
from ottomen.algorithm.experiment import new_experiment, new_task

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
        new_experiment(1337, 0.98)
        new_task('1337',1337)