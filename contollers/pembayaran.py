import datetime
import traceback
import validators
from flask import Flask, jsonify, request
from flask import Blueprint
from common.baseResponse import BaseResponse
from common.baseResponseSingle import BaseResponseSingle
from common.errorResponse import ErrorResponse
from models.pembayaran import Pembayaran
from schema.pembayaranSchema import PembayaranSchema
from schema.userSchema import UserSchema
from app import db
from services.logActivityService import LogActivityService
from services.kelasService import KelasService
from services.userService import UserService
from services.pembayaranService import PembayaranService
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

ts = datetime.datetime.utcnow()

pembayaran_api = Blueprint('pembayaran_api', __name__)

@pembayaran_api.route("/pembayaran", methods=["GET"])
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
        pembayaran_schema = PembayaranSchema(many=True)
        data = PembayaranService.get_list(search, page, limit, sortBy) 
        print(pembayaran_schema.dump(data))
        return jsonify(
            BaseResponse(
                pembayaran_schema.dump(data),
                "Pembayaran successfully Show",
                page,
                limit,
                len(pembayaran_schema.dump(data)),
                200,
            ).serialize()
        ), 200

    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
@pembayaran_api.route('/pembayaran/<string:id>', methods=["GET"])
def get_by_id(id):
    try:
        data = PembayaranService.get_by_id(id) 
        if not data:
            return ErrorResponse(exception="Pembayaran is Not Found", code=400).serialize()
        pembayaran_schema = PembayaranSchema()
        return (
            jsonify(
                BaseResponseSingle(
                    pembayaran_schema.dump(data),
                    "Pembayaran successfully Showed",
                    200,
                ).serialize()
            ),
            200
        )
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
@pembayaran_api.route('/pembayaran', methods=["POST"]) 
# @jwt_required()
def pembayaran():
    try:
        pembayaran_schema = PembayaranSchema()
        pembayaran = pembayaran_schema.load(request.json)

        if not pembayaran.get('tgl_bayar'):
            return ErrorResponse(exception="Tanggal is Required", code=400).serialize()
        if not pembayaran.get('bulan_bayar'):
            return ErrorResponse(exception="Bulan is Required", code=400).serialize()
        if not pembayaran.get('tahun_bayar'):
            return ErrorResponse(exception="Tahun is Required", code=400).serialize()  
        if not pembayaran.get('jumlah_bayar'):
            return ErrorResponse(exception="Jumlah is Required", code=400).serialize()      
        if not pembayaran.get('name'):
            return ErrorResponse(exception="Name is Required", code=400).serialize()  
       
        user = UserService.get_by_name(name=pembayaran.get("name"))

        add_pembayaran = Pembayaran(
            user_id=user.id,
            tgl_bayar=pembayaran['tgl_bayar'],
            bulan_bayar=pembayaran['bulan_bayar'],
            tahun_bayar=pembayaran["tahun_bayar"],
            jumlah_bayar=pembayaran["jumlah_bayar"],
            created_at=ts,
            updated_at=None,
            deleted_at=None,
            last_login_at=None
        )

        db.session.add(add_pembayaran)
        db.session.commit()

        data = pembayaran_schema.dump(add_pembayaran)
        data["name"] = user.name # Add user name to the data dictionary
        
        return jsonify(
            BaseResponseSingle(
                data,
                "Pembayaran Successfully",
                200
            ).serialize()
        ), 200

    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
