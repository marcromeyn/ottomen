from . import OttomenResourceTestCase
from ottomen.resources.services import *
from werkzeug.exceptions import HTTPException
import sure
import pytest
from helpers import create_worker


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
            exp = workers.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            workers.get_or_404('10000000')
