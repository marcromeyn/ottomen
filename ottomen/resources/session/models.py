from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer


class Session(JsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "session"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    turk_id = db.Column(db.String, db.ForeignKey("worker.id"))
    task_id = db.Column(db.String, db.ForeignKey("task.id"))
    task = db.relationship("Task", foreign_keys=[task_id], backref="sessions")
    turk = db.relationship("Worker", foreign_keys=[turk_id], backref="sessions")
