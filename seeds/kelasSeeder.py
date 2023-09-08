from datetime import datetime
import traceback
from flask_seeder import Seeder
from app import db
from models.kelas import Kelas
import uuid

class KelasSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        ts = datetime.utcnow()
        try:
            print("adding Kelas")
            
            kelas = Kelas.query.all()
            if len(kelas) == 0:
                kelas_data = [
                    Kelas(
                        kelas="X RPL 1",
                        created_at=ts,
                        deleted_at=None,
                        updated_at=None
                    ),
                    Kelas(
                        kelas="X DPIB 1",
                        created_at=ts,
                        deleted_at=None,
                        updated_at=None
                    ),
                    Kelas(
                        kelas="X TAV 1",
                        created_at=ts,
                        deleted_at=None,
                        updated_at=None
                    ),
                    Kelas(
                        kelas="X TBSM 1",
                        created_at=ts,
                        deleted_at=None,
                        updated_at=None
                    ),
                    Kelas(
                        kelas="X TKR 1",
                        created_at=ts,
                        deleted_at=None,
                        updated_at=None
                    ),
                ]
                db.session.bulk_save_objects(kelas_data)
                db.session.commit()
        except Exception as e:
           traceback.print_exc()
