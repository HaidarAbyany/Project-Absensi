from sqlalchemy import ForeignKey
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json
import uuid

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kelas_id = db.Column(UUID(as_uuid=True), ForeignKey('kelas.id'))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    gender = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(255), default=None)
    created_at = db.Column(db.DateTime(), nullable=True, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), nullable=True)
    deleted_at = db.Column(db.DateTime(), nullable=True)
    last_login_at = db.Column(db.DateTime(), nullable=True)

    kelas = relationship("Kelas", backref="users")
    # parent_clientId = db.Column(UUID(as_uuid=True), nullable=True)

   

    def __init__(
        self,
        kelas_id,
        name,
        email,
        password,
        gender,
        token,
        deleted_at,
        created_at,
        updated_at,
        last_login_at,
    ):
        self.name = name
        self.kelas_id = kelas_id
        self.email = email
        self.password = password
        self.gender = gender
        self.token = token
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login_at = last_login_at

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<id {}>".format(self.id)