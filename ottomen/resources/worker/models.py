from ...core import db
from .. import ResourceMixin
from ...helpers import JsonSerializer


class WorkerJsonSerializer(JsonSerializer):
    __json_public__ = ['id', 'tw_pos', 'tw_neg', 'class_pos', 'class_neg', 'banned', 'timestamp']


class Worker(WorkerJsonSerializer, ResourceMixin, db.Model):
    __tablename__ = "worker"

    id = db.Column(db.String, primary_key=True)
    tw_pos = db.Column(db.Float, default=1)
    tw_neg = db.Column(db.Float, default=1)
    class_pos = db.Column(db.Integer, default=1)
    class_neg = db.Column(db.Integer, default=1)
    # session_id = db.Column(db.Integer, ForeignKey("session.id"))
    banned = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime)
