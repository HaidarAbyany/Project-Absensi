from sqlalchemy import ForeignKey
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import datetime
import json
import uuid

class Pembayaran(db.Model):
    __tablename__ = "pembayaran"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'))    
    tgl_bayar = db.Column(db.String(30))
    bulan_bayar = db.Column(db.String(30))
    tahun_bayar = db.Column(db.String(30))
    jumlah_bayar = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(), nullable=True, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime(), nullable=True)
    deleted_at = db.Column(db.DateTime(), nullable=True)
    last_login_at = db.Column(db.DateTime(), nullable=True)

    user = relationship("Users", backref="pembayaran")
   
    # parent_clientId = db.Column(UUID(as_uuid=True), nullable=True)

   

    def __init__(
        self,
        user_id,
        tgl_bayar,
        bulan_bayar,
        tahun_bayar,
        jumlah_bayar,
        deleted_at,
        created_at,
        updated_at,
        last_login_at,
    ):
        self.user_id = user_id
        self.tgl_bayar = tgl_bayar
        self.bulan_bayar = bulan_bayar
        self.tahun_bayar = tahun_bayar
        self.jumlah_bayar = jumlah_bayar
        self.deleted_at = deleted_at
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login_at = last_login_at

    def __repr__(self):
        return "<id {}>".format(self.id)