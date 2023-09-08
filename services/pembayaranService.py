from app import db
from models.pembayaran import Pembayaran
from sqlalchemy.sql import text

class PembayaranService(db.Model):
    __tablename__ = "pembayaran"

    def get_list(filter, page, limit, sortBy):
        search = "%{}%".format(filter)
        data = Pembayaran.query.filter(
            Pembayaran.deleted_at == None,
            Pembayaran.jumlah_bayar.ilike(search)
        )
       
        if sortBy is not None:
            sortBy = sortBy.split(",")
            data = data.order_by(text("{} {}".format(sortBy[0], sortBy[1])))
        paginated_data = data.paginate(page=page, per_page=limit)

        return paginated_data
    
    def get_by_id(id):
        data = Pembayaran.query.filter_by(id = id).first()

        return data
    
