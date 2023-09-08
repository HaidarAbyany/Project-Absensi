import datetime
import traceback
import validators
from flask import Flask, jsonify, request
from flask import Blueprint
from common.baseResponse import BaseResponse
from common.baseResponseSingle import BaseResponseSingle
from common.errorResponse import ErrorResponse
from models.user import Users
from schema.userSchema import UserSchema
from app import db
from services.logActivityService import LogActivityService
from services.kelasService import KelasService
from services.userService import UserService
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

ts = datetime.datetime.utcnow()

auth_api = Blueprint('auth_api', __name__)

@auth_api.route("/users", methods=["GET"])
def get_list():

    args = request.args
    search = args.get("search", "")
    page = args.get("page", 1)
    try:
        page = int(page)
    except ValueError:
        pass
    limit = args.get("limit", 10)
    try:
        limit = int(limit)
    except ValueError:
        pass
    sortBy = args.get("sortBy", "id,desc")
        
    try:
        user_schema = UserSchema(many=True)
        data = UserService.get_list(search, page, limit, sortBy) 
        print(user_schema.dump(data))
        return jsonify(
            BaseResponse(
                user_schema.dump(data),
                "User successfully Show",
                page,
                limit,
                len(user_schema.dump(data)),
                200,
            ).serialize()
        ), 200

    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
@auth_api.route('/users/<string:id>', methods=["GET"])
def get_by_id(id):
    try:
        data = UserService.get_by_id(id) 
        if not data:
            return ErrorResponse(exception="Kelas is Not Found", code=400).serialize()
        user_schema = UserSchema()
        return (
            jsonify(
                BaseResponseSingle(
                    user_schema.dump(data),
                    "User successfully Showed",
                    200,
                ).serialize()
            ),
            200
        )
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())

@auth_api.route("/login", methods=["POST"])
def login():
    json = request.json

    try:
        if not request or not request.json["email"] or not request.json["password"]:
            return jsonify({"message": "username or password is missing","status": 400}),400
        
        user = UserService.get_by_email(email=json.get("email"))

        if user:
            if not user.checkPassword(json.get("password")):
                return jsonify({"message": "email or password is invalid", "status": 400}),400 
            else:
                expires_token = datetime.timedelta(days=1)
                expires_refresh = datetime.timedelta(days=3)
                access_token = create_access_token(identity=user.id, expires_delta=expires_token)
                refresh_token = create_refresh_token(identity=user.id, expires_delta=expires_refresh)
                user.last_login_at = ts
                db.session.commit()
        else:
            return jsonify({"message": "Credentials not found", "status": 400}),400
        
        LogActivityService.add_log(user_id=user.id, activity=f"{user.name} login to system")
        
        return jsonify({
            'message': 'Login successful',
            'status': 200,
            'data': 
                {
                'user_id': user.id,
                'username': user.name,
                'access_token': access_token,
                'refresh_token': refresh_token,
                }
        }), 200
    
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize()) 
    
@auth_api.route('/register', methods=["POST"]) 
# @jwt_required()
def register():
    try:
        user_schema = UserSchema()
        user = user_schema.load(request.json)

        if not user.get('email'):
            return ErrorResponse(exception="Email is Required", code=400).serialize()
        if not user.get('password'):
            return ErrorResponse(exception="Password is Required", code=400).serialize()
        if not user.get('kelas'):
            return ErrorResponse(exception="Kelas is Required", code=400).serialize()

        user_validator = UserService.get_by_email(user['email'])
        if not validators.email(user.get('email')):
            return ErrorResponse(exception="Email is not Valid", code=400).serialize()
        if user_validator:
            return ErrorResponse(exception="Email Already Registered", code=400).serialize()
        
        
        

        kelas = KelasService.get_by_kelas(kelas=user.get("kelas"))

        add_user = Users(
            kelas_id=kelas.id,
            name=user['name'],
            email=user['email'],
            password=user.get("password"),
            gender=None,
            created_at=ts,
            updated_at=None,
            deleted_at=None,
            token=None,
            last_login_at=None
        )

        add_user.setPassword(password=user.get("password"))

        db.session.add(add_user)
        db.session.commit()

        data = user_schema.dump(add_user)
        data.pop("password", None)  # Remove the 'password' field from the data dictionary

        data["kelas"] = kelas.kelas # Add role name to the data dictionary

        return jsonify(
            BaseResponseSingle(
                data,
                "Register Successfully",
                200
            ).serialize()
        ), 200

    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
@auth_api.route("/refresh_token", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_auth = get_jwt_identity()
        new_token = create_access_token(identity=user_auth, fresh=True)

        return jsonify({
            "message": "refresh token", 
            "status": 200, 
            "data": {
                "token": new_token,
                }
        })
    except Exception as e:
        response = BaseResponse(None, str(e), 0, 0, 0, False)
        return jsonify(response.serialize())
    
@auth_api.route('/logout/<string:id>', methods=["PUT"])
def logout_user(id):
    
    try:
        data = LogActivityService.get_by_id(id)
        if data.deleted_at is not None:
            return ErrorResponse(exception="User is Not Found", code=400).serialize()
        
        data.deleted_at = ts
        db.session.commit()

        return (
            jsonify(
                BaseResponseSingle(
                    data.id,
                    "User successfully Logout",
                    200,
                ).serialize()
            ),
            200
        )
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())






