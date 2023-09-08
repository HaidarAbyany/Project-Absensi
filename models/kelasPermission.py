from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db

class KelasPermission(db.Model):
    __tablename__ = "kelas_permission"

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    kelas_id = db.Column(UUID(as_uuid=True) , ForeignKey('kelas.id'))
    permission_id = db.Column(db.String(36), ForeignKey('permission.id'))
    created_at = db.Column(db.DateTime(), nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), nullable=True)
    deleted_at = db.Column(db.DateTime(), nullable=True)

    kelas = relationship("Kelas", backref="kelas_permission")
    permission = relationship("Permission", backref="kelas_permission")

    def __init__(self, kelas_id, permission_id, created_at, updated_at, deleted_at):
        self.kelas_id = kelas_id,
        self.permission_id = permission_id,
        self.created_at = created_at,
        self.updated_at = updated_at,
        self.deleted_at = deleted_at,

    def __repr__(self):
        return "<id {}>".format(self.id)
