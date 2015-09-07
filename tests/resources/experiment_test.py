from . import OttomenResourceTestCase
from ottomen.resources.services import experiments
import sure


class ExperimentResourceTestCase(OttomenResourceTestCase):
    def test_db_create(self):
        exp = experiments.new(description="A shitty description", accuracy=.7)
        exp.shouldnt.be(())
        exp.id.should.be(None)

        exp_db = experiments.save(exp)
        # exp_db.shouldnt.be(())
        # exp_db.id.shouldnt.be(None)
        # a = 5
