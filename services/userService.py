from app import db
from models.user import Users
from sqlalchemy.sql import text

class UserService(db.Model):
    __tablename__ = "users"

    def get_list(filter, page, limit, sortBy):
        search = "%{}%".format(filter)
        data = Users.query.filter(
            Users.deleted_at == None,
            Users.name.ilike(search)
        )
       
        if sortBy is not None:
            sortBy = sortBy.split(",")
            data = data.order_by(text("{} {}".format(sortBy[0], sortBy[1])))
        paginated_data = data.paginate(page=page, per_page=limit)

        return paginated_data
    
    def get_by_id(id):
        data = Users.query.filter_by(id = id).first()

        return data
    
    def get_by_email(email):
        data = Users.query.filter_by(email = email).first()
        return data
    
    def get_by_name(name):
        data = Users.query.filter_by(name = name).first()
       
        return data