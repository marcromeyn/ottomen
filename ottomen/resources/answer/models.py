from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer

answer_output = db.Table("answer_output",
                         db.Column("answer_id", db.Integer, db.ForeignKey("answer.id")),
                         db.Column("output_id", db.Integer, db.ForeignKey("output.id")))


class AnswerJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'timestamp', 'question', 'outputs', 'worker']


class Answer(AnswerJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "answer"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    worker_id = db.Column(db.String, db.ForeignKey("worker.id"))

    outputs = db.relationship("Output", secondary=answer_output, backref="answers")
    question = db.relationship("Question", foreign_keys=[question_id], backref="answers")
    worker = db.relationship("Worker", foreign_keys=[worker_id], backref="answers")


class Output(JsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "output"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
