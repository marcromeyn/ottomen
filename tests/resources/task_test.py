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
        task_mem = tasks.new_mem(task_db).get()
        task_mem['id'].should.be.equal(task_db.id)
        task_mem['experiment_id'].should.be.equal(task_db.experiment_id)
        task_mem['batch_size'].should.be.equal(task_db.batch_size)
        task_mem['nr_of_batches'].should.be.equal(task_db.nr_of_batches)
        task_mem['size'].should.be.equal(task_db.size)
        task_mem['initial_consensus'].should.be.equal(task_db.initial_consensus)
        task_mem['returning_consensus'].should.be.equal(task_db.returning_consensus)
        task_mem['minimum_mt_score'].should.be.equal(task_db.minimum_mt_score)
        task_mem['minimum_mt_submissions'].should.be.equal(task_db.minimum_mt_submissions)
        task_mem['reward'].should.be.equal(task_db.reward)
        task_mem['title'].should.be.equal(task_db.title)
        task_mem['description'].should.be.equal(task_db.description)
        task_mem['url'].should.be.equal(task_db.url)
        tasks.get_mem_obj(task_db.id).id.should.be.equal(task_db.id)

    def test_new_mem_malformed_model(self):
        with pytest.raises(TypeError):
            t = tasks.new_mem({'not_there': True})

    def test_update_mem(self):
        task_db = create_task()
        task_mem = tasks.new_mem(task_db).get()
        new_id = 'new_shitty_id'
        task_mem['id'] = new_id
        tasks.update_mem(task_mem)
        tasks.get_mem_obj(new_id).id.should.be.equal(new_id)

    def test_update_mem_malformed_model(self):
        task_db = create_task()
        task_mem = tasks.new_mem(task_db).get()
        task_mem['key_that_doesnt_exist_in_model'] = 'new_shitty_value'

        with pytest.raises(TypeError):
            tasks.update_mem(task_mem)

    # def test_access_experiment(self):
    #     task_db = create_task()
    #     exp_mem = experiments.new_mem(task_db.experiment)
    #     task_mem = tasks.new_mem(task_db)
    #     int(task_mem.experiment()['id']).should.be.equal(task_db.experiment_id)
