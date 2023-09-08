import datetime
from app import db
from models.logActivity import LogActivity
from sqlalchemy.sql import text

ts = datetime.datetime.utcnow()

class LogActivityService(db.Model):
    __tablename__ = "log_activity"

    def add_log(user_id, activity):
        log = LogActivity(
            user_id = user_id,
            activity = activity,
            created_at = ts,
            deleted_at= None
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    def get_list(filter, page, limit, sortBy):
        search = "%{}%".format(filter)
        data = LogActivity.query.filter(
            LogActivity.deleted_at == ts,
            LogActivity.kelas.ilike(search)
        )
       
        if sortBy is not None:
            sortBy = sortBy.split(",")
            data = data.order_by(text("{} {}".format(sortBy[0], sortBy[1])))
        paginated_data = data.paginate(page=page, per_page=limit)

        return paginated_data
    
    def get_by_id(id):
        data = LogActivity.query.filter_by(id = id).first()

        return data
