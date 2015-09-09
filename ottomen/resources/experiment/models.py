from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer

experiment_question = db.Table("experiment_question",
                               db.Column("experiment_id", db.Integer, db.ForeignKey("experiment.id")),
                               db.Column("question_id", db.Integer, db.ForeignKey("question.id")))


class ExperimentJsonSerializer(JsonSerializer):
    # __json_public__ = ['id', 'description', 'end_date', 'completed', 'accuracy', 'questions']
    __json_other_models__ = ['questions', 'validations']


class Experiment(ExperimentJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "experiment"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    end_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    accuracy = db.Column(db.Float, nullable=False)

    questions = db.relationship("Question", secondary=experiment_question, backref="experiments")
