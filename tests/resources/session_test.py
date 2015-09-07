from . import OttomenResourceTestCase
from ottomen.resources.services import *
from werkzeug.exceptions import HTTPException
import sure
import pytest
from helpers import create_session, create_worker


class SessionResourceTestCase(OttomenResourceTestCase):
    def test_db_create(self):
        """
        It should be able to insert a answer in the database and successfully retrieve it
        """
        session_db = create_session()
        session_db.id.should.be.greater_than(0)
        sessions.find(id=session_db.id).shouldnt.be(None)
        sessions.get(id=session_db.id).shouldnt.be(None)

    def test_db_delete(self):
        """
        It should be able to delete a answer from the database
        """
        session_db = create_session()

        to_delete = sessions.delete(session_db)
        to_delete.should.be(None)
        deleted = sessions.get(id=session_db.id)
        deleted.should.be(None)

    def test_db_update(self):
        session_db = create_session()
        new_worker = create_worker()
        updated = sessions.update(session_db, worker=new_worker)
        updated.worker.id.should_not.be.different_of(new_worker.id)

    def test_malformed_model(self):
        with pytest.raises(TypeError):
            exp = sessions.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            sessions.get_or_404(10000000)


