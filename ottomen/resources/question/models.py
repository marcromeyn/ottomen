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

validation_malware = db.Table("validation_malware",
                         db.Column("validation_id", db.Integer, db.ForeignKey("validation.id")),
                         db.Column("malware_id", db.Integer, db.ForeignKey("malware.id")))


class Validation(db.Model):
    __tablename__ = "validation"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    experiment_id = db.Column(db.Integer, db.ForeignKey("experiment.id"))
    malware = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    malwares = db.relationship("Malware", secondary=validation_malware)
    experiment = db.relationship("Experiment", foreign_keys=[experiment_id], backref="validations")
    question = db.relationship("Question", foreign_keys=[question_id], backref="validations")
