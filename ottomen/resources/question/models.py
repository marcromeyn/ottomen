from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer


class QuestionJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'belief', 'in_progress', 'text']


class Question(QuestionJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    belief = db.Column(db.Boolean, default=True)
    in_progress = db.Column(db.Boolean, default=False)
    text = db.Column(db.String)


validation_output = db.Table("validation_label",
                             db.Column("validation_id", db.Integer, db.ForeignKey("validation.id")),
                             db.Column("label_id", db.Integer, db.ForeignKey("label.id")))


class Validation(JsonSerializer, db.Model):
    __tablename__ = "validation"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    experiment_id = db.Column(db.Integer, db.ForeignKey("experiment.id"))
    label = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    labels = db.relationship("Label", secondary=validation_output)
    experiment = db.relationship("Experiment", foreign_keys=[experiment_id], backref="validations")
    question = db.relationship("Question", foreign_keys=[question_id], backref="validations")
