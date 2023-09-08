from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config.from_pyfile('config.py')

jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app=app, db=db)
seeder = FlaskSeeder(app=app, db=db)
seeder.init_app(app=app, db=db)

# @jwt.expired_token_loader
# def my_expired_token_callback(jwt_header, jwt_payload):
#     response = BaseResponse(None, "Token Expired", 0, 0, 0, 401)
#     return jsonify(response.serialize()), 401


# @jwt.unauthorized_loader
# def my_unauthorize_callback(jwt_header):
#     response = BaseResponse(None, "Unauthorize", 0, 0, 0, 401)
#     return jsonify(response.serialize()), 401


# def method_not_allowed_exception(e):
#     response = BaseResponse(None, "Method not Allowed", 0, 0, 0, 401)
#     return jsonify(response.serialize()), 405


# def notfound_exception(e):
#     response = BaseResponse(None, "Endpoint Not Found", 0, 0, 0, 401)
#     return jsonify(response.serialize()), 404

# @app.errorhandler(Exception)
# def handle_exception(e):
#     res = BaseResponse(None, str(e), 0, 0, 0, 401).serialize()
#     return jsonify(res), 500

# app.register_error_handler(404, notfound_exception)
# app.register_error_handler(405, method_not_allowed_exception)

#membuat model database authentikasi (login, register)

from contollers.auth import auth_api
from contollers.kelas import kelas_api
from contollers.pembayaran import pembayaran_api


path_api = "/api/v1"

app.register_blueprint(auth_api , url_prefix=path_api)
app.register_blueprint(kelas_api , url_prefix=path_api)
app.register_blueprint(pembayaran_api , url_prefix=path_api)



if __name__ == '__main__':
    app.run()