from . import OttomenResourceTestCase
from ottomen.resources.services import *
from werkzeug.exceptions import HTTPException
import sure
import pytest
from helpers import create_worker, create_experiment


class WorkerResourceTestCase(OttomenResourceTestCase):
    def test_db_create(self):
        """
        It should be able to insert a answer in the database and successfully retrieve it
        """
        worker_db = create_worker()
        worker_db.id.should.be.greater_than(0)
        workers.find(id=worker_db.id).shouldnt.be(None)
        workers.get(id=worker_db.id).shouldnt.be(None)

    def test_db_delete(self):
        """
        It should be able to delete a answer from the database
        """
        worker_db = create_worker()

        to_delete = workers.delete(worker_db)
        to_delete.should.be(None)
        deleted = workers.get(id=worker_db.id)
        deleted.should.be(None)

    def test_db_update(self):
        worker_db = create_worker()
        updated = workers.update(worker_db, tw_pos=.8)
        updated.tw_pos.should.be.equal(.8)

    def test_malformed_model(self):
        with pytest.raises(TypeError):
            w = workers.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            workers.get_or_404('10000000')

    def test_new_mem(self):
        worker_db = create_worker()
        exp_db = create_experiment()
        worker_mem = workers.new_mem(exp_db.id, worker_db).get()
        worker_mem['id'].should.be.equal(worker_db.id)
        worker_mem['tw_pos'].should.be.equal(worker_db.tw_pos)
        worker_mem['tw_neg'].should.be.equal(worker_db.tw_neg)
        worker_mem['class_pos'].should.be.equal(worker_db.class_pos)
        worker_mem['class_neg'].should.be.equal(worker_db.class_neg)
        worker_mem['banned'].should.be.equal(worker_db.banned)
        worker_mem['timestamp'].should.be.equal(worker_db.timestamp)
        workers.get_mem_obj(exp_db.id, worker_mem['id']).id.should.be.equal(worker_db.id)

    def test_new_mem_malformed_model(self):
        with pytest.raises(TypeError):
            exp_db = create_experiment()
            t = workers.new_mem(exp_db.id, {'not_there': True})

    def test_update_mem(self):
        worker_db = create_worker()
        exp_db = create_experiment()
        worker_mem = workers.new_mem(exp_db.id, worker_db).get()
        new_id = 'new_shitty_id'
        worker_mem['id'] = new_id
        workers.update_mem(exp_db.id, worker_mem)
        workers.get_mem_obj(exp_db.id, new_id).id.should.be.equal(new_id)

    def test_update_mem_malformed_model(self):
        worker_db = create_worker()
        exp_db = create_experiment()
        worker_mem = workers.new_mem(exp_db.id, worker_db).get()
        worker_mem['key_that_doesnt_exist_in_model'] = 'new_shitty_value'

        with pytest.raises(TypeError):
            workers.update_mem(exp_db.id, worker_mem)
