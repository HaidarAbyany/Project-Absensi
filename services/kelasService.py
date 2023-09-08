from app import db
from models.kelas import Kelas
from sqlalchemy.sql import text

class KelasService(db.Model):
    __tablename__ = "kelas"

    def get_list(filter, page, limit, sortBy):
        search = "%{}%".format(filter)
        data = Kelas.query.filter(
            Kelas.deleted_at == None,
            Kelas.kelas.ilike(search)
        )
       
        if sortBy is not None:
            sortBy = sortBy.split(",")
            data = data.order_by(text("{} {}".format(sortBy[0], sortBy[1])))
        paginated_data = data.paginate(page=page, per_page=limit)

        return paginated_data
    
    def get_by_id(id):
        data = Kelas.query.filter_by(id = id).first()

        return data
    
    def get_by_kelas(kelas):
        data = Kelas.query.filter_by(kelas = kelas).first()
       
        return data