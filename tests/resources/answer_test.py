from . import OttomenResourceTestCase
from ottomen.resources.services import experiments, workers, answers
from werkzeug.exceptions import HTTPException
import sure
import pytest
from helpers import create_answer, create_label


class AnswerResourceTestCase(OttomenResourceTestCase):
    def test_db_create(self):
        """
        It should be able to insert a answer in the database and successfully retrieve it
        """
        ans_db = create_answer()
        len(answers.all()).should.be.greater_than(0)
        answers.find(id=ans_db.id).shouldnt.be(None)
        answers.get(id=ans_db.id).shouldnt.be(None)

    def test_db_delete(self):
        """
        It should be able to delete a answer from the database
        """
        ans_db = create_answer()

        to_delete = answers.delete(ans_db)
        to_delete.should.be(None)
        deleted = answers.get(id=ans_db.id)
        deleted.should.be(None)

    def test_db_update(self):
        ans_db = create_answer()
        new_label = create_label(name='Label2')
        updated = answers.update(ans_db, labels=[new_label])
        updated.labels[0].name.should.be.equal('Label2')

    def test_malformed_model(self):
        with pytest.raises(TypeError):
            exp = answers.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            answers.get_or_404(10000000)


