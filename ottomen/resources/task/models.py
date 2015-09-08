from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer

class TaskJsonSerializer(JsonSerializer):
    # __json_public__ = ['id', 'belief', 'in_progress', 'text']
    __json_othermodels__ = ['experiment']

class Task(TaskJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "task"

    id = db.Column(db.String, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey("experiment.id"))
    batch_size = db.Column(db.Integer, default=10)
    nr_of_batches = db.Column(db.Integer, default=5)
    size = db.Column(db.Integer, default=50)
    initial_consensus = db.Column(db.Integer, default=30)
    returning_consensus = db.Column(db.Integer, default=10)
    minimum_mt_score = db.Column(db.Float, default=.95)
    minimum_mt_submissions = db.Column(db.Integer, default=500)

    reward = db.Column(db.Float, default=.5)
    title = db.Column(db.String)
    description = db.Column(db.String)
    url = db.Column(db.String)

    experiment = db.relationship("Experiment", foreign_keys=[experiment_id])

