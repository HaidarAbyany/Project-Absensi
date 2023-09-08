from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class Kelas(db.Model):
    __tablename__ = "kelas"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kelas = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), nullable=True)
    deleted_at = db.Column(db.DateTime(), nullable=True)

    def __init__(self, kelas, created_at, updated_at, deleted_at):
        self.kelas = kelas,
        self.created_at = created_at,
        self.updated_at = updated_at,
        self.deleted_at = deleted_at,

    def __repr__(self):
        return "<id {}>".format(self.id)
