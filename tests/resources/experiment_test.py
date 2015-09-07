from . import OttomenResourceTestCase
from ottomen.resources.services import experiments
from werkzeug.exceptions import HTTPException
import sure
import pytest
from .helpers import create_experiment


class ExperimentResourceTestCase(OttomenResourceTestCase):
    def test_db_create(self):
        """
        It should be able to insert a experiment in the database and successfully retrieve it
        """
        exp_db = create_experiment()
        exp_db.shouldnt.be(())
        exp_db.id.shouldnt.be(None)
        len(experiments.all()).should.be.greater_than(0)
        experiments.find(id=exp_db.id).shouldnt.be(None)
        experiments.get(id=exp_db.id).shouldnt.be(None)

    def test_db_delete(self):
        exp_db = create_experiment()
        exp_db.shouldnt.be(())
        exp_db.id.shouldnt.be(None)

        to_delete = experiments.delete(exp_db)
        to_delete.should.be(None)
        deleted = experiments.get(id=exp_db.id)
        deleted.should.be(None)

    def test_db_update(self):
        exp = create_experiment()
        updated = experiments.update(exp, accuracy=.9)
        updated.accuracy.should.be.equal(.9)
        experiments.get(exp.id).accuracy.should.be.equal(.9)

    def test_malformed_model(self):
        with pytest.raises(TypeError):
            exp = experiments.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            experiments.get_or_404(10000000)


