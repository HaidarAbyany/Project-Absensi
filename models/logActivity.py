from datetime import datetime
from email.policy import default

from sqlalchemy import ForeignKey
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class LogActivity(db.Model):
    __tablename__ = "log_activity"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'))
    activity = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.utcnow())
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)

    def __init__(self, user_id, activity, created_at, deleted_at):
        self.user_id = user_id
        self.activity = activity
        self.created_at = created_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return "<id {}>".format(self.id)
