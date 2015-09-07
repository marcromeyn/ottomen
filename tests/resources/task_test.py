from . import OttomenResourceTestCase
from ottomen.resources.services import *
from werkzeug.exceptions import HTTPException
import sure
import pytest
from helpers import create_task, create_experiment


class TaskResourceTestCase(OttomenResourceTestCase):
    def test_db_create(self):
        """
        It should be able to insert a answer in the database and successfully retrieve it
        """
        task_db = create_task()
        task_db.id.should.be.greater_than(0)
        tasks.find(id=task_db.id).shouldnt.be(None)
        tasks.get(id=task_db.id).shouldnt.be(None)

    def test_db_delete(self):
        """
        It should be able to delete a answer from the database
        """
        task_db = create_task()

        to_delete = tasks.delete(task_db)
        to_delete.should.be(None)
        deleted = tasks.get(id=task_db.id)
        deleted.should.be(None)

    def test_db_update(self):
        task_db = create_task()
        new_experiment = create_experiment()
        updated = tasks.update(task_db, experiment=new_experiment)
        updated.experiment.id.should.be.equal(new_experiment.id)

    def test_malformed_model(self):
        with pytest.raises(TypeError):
            t = tasks.new(description="A shitty description", accuracy=.7, not_there=5)

    def test_404(self):
        with pytest.raises(HTTPException):
            tasks.get_or_404('10000000')

    def test_new_mem(self):
        task_db = create_task()
        task_mem = tasks.new_mem(task_db.to_json())
        task_mem.get()['id'].should.be.equal(task_db.id)

    def test_access_experiment(self):
        task_db = create_task()
        exp_mem = experiments.new_mem(task_db.experiment.to_json())
        task_mem = tasks.new_mem(task_db.to_json())
        int(task_mem.experiment()['id']).should.be.equal(task_db.experiment_id)
