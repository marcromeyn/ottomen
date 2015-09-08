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
            
    def test_new_mem(self):
        exp_db = create_experiment()
        exp_mem = experiments.new_mem(exp_db).get()
        exp_mem['id'].should.be.equal(exp_db.id)
        exp_mem['description'].should.be.equal(exp_db.description)
        # exp_mem['end_date'].should.be.equal(exp_db.end_date)
        exp_mem['completed'].should.be.equal(exp_db.completed)
        exp_mem['accuracy'].should.be.equal(exp_db.accuracy)
        experiments.get_mem(exp_db.id).get()['id'].should.be.equal(exp_db.id)

    def test_new_mem_malformed_model(self):
        with pytest.raises(ValueError):
            t = experiments.new_mem({'id': 'wrong_object'})

    def test_update_mem(self):
        exp_db = create_experiment()
        exp_mem = experiments.new_mem(exp_db).get()
        new_id = 500000
        exp_mem['id'] = new_id
        experiments.update_mem(exp_mem)
        experiments.get_mem(new_id).get()['id'].should.be.equal(new_id)

    def test_update_mem_malformed_model(self):
        exp_id = create_experiment()
        exp_mem = experiments.new_mem(exp_id).get()
        exp_mem['key_that_doesnt_exist_in_model'] = 'new_shitty_value'

        with pytest.raises(TypeError):
            experiments.update_mem(exp_mem)


