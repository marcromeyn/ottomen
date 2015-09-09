from . import OttomenResourceTestCaseWithPopulatedDb
from ottomen.resources.services import *
from werkzeug.exceptions import HTTPException
import sure
import pytest
from helpers import create_question


class QuestionResourceTestCase(OttomenResourceTestCaseWithPopulatedDb):
    def test_db_create(self):
        """
        It should be able to insert a answer in the database and successfully retrieve it
        """
        question_db = create_question()
        question_db.id.should.be.greater_than(0)
        questions.find(id=question_db.id).shouldnt.be(None)
        questions.get(id=question_db.id).shouldnt.be(None)

    def test_db_delete(self):
        """
        It should be able to delete a answer from the database
        """
        question_db = create_question()

        to_delete = questions.delete(question_db)
        to_delete.should.be(None)
        deleted = questions.get(id=question_db.id)
        deleted.should.be(None)

    def test_db_update(self):
        question_db = create_question()
        updated = questions.update(question_db, text='ottomoney')
        updated.text.should.be.equal('ottomoney')

    def test_malformed_model(self):
        with pytest.raises(TypeError):
            qs = questions.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            questions.get_or_404(10000000)

    def test_get_unanswered_consensus(self):
        response = questions.get_unanswered_consensus(0, "gayturk", 10)
        len(response).should.equal(10)
        response.should.be.a('list')
        for q in response:
            q.id.should.be.an('int')
        # non-existing experiment
        response = questions.get_unanswered_consensus(100, "gayturk", 0)
        len(response).should.equal(0)

    def test_get_positive(self):
        response = questions.get_positive(1337, 400)
        len(response).should.equal(400)
        response.should.be.a('list')
        for q in response:
            q.experiments[0].id.should.equal(1337)
            q.belief.should.equal(True)

    def test_get_negative(self):
        response = questions.get_negative(1337, 400)
        len(response).should.equal(400)
        response.should.be.a('list')
        for q in response:
            q.experiments[0].id.should.equal(1337)
            q.belief.should.equal(False)

    def test_get_control_positive(self):
        response = questions.get_control_positive(0, 20)
        len(response).should.equal(20)
        response.should.be.a('list')
        for q in response:
            q.validations[0].experiment_id.should.be(0)
            q.validations[0].label.should.be(True)
            len(q.validations[0].labels).should.be.greater_than(0)

    def test_get_control_negative(self):
        response = questions.get_control_negative(0, 20)
        len(response).should.equal(20)
        response.should.be.a('list')
        for q in response:
            q.validations[0].experiment_id.should.be(0)
            q.validations[0].label.should.be(False)
            q.validations[0].labels.should.be.empty





