from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer

answer_label = db.Table("answer_label",
                        db.Column("answer_id", db.Integer, db.ForeignKey("answer.id")),
                        db.Column("label_id", db.Integer, db.ForeignKey("label.id")))


class AnswerJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'timestamp', 'question', 'labels', 'worker']
    __json_other_models__ = ['labels', 'question', 'worker']


class Answer(AnswerJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "answer"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    worker_id = db.Column(db.String, db.ForeignKey("worker.id"))

    labels = db.relationship("Label", secondary=answer_label, backref="answers")
    question = db.relationship("Question", foreign_keys=[question_id], backref="answers")
    worker = db.relationship("Worker", foreign_keys=[worker_id], backref="answers")


class Label(JsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "label"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
