from datetime import datetime
from email.policy import default
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Permission(db.Model):
    __tablename__ = "permission"

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String())
    slug = db.Column(db.String())
    module = db.Column(db.String())
    created_at = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(
        db.TIMESTAMP(),
        nullable=False,
        onupdate=datetime.utcnow(),
        default=datetime.utcnow(),
    )
    deleted_at = db.Column(db.TIMESTAMP(), nullable=True)

    def __init__(self, name, slug, module, created_at, updated_at, deleted_at):
        self.name = name
        self.slug = slug
        self.module = module
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return "<id {}>".format(self.id)

    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "slug": self.slug,
    #         "module": self.module,
    #         "created_at": self.created_at,
    #         "updated_at": self.updated_at,
    #         "deleted_at": self.deleted_at,
    #     }
