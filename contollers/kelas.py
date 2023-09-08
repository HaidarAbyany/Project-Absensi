import datetime
import json
import traceback
from flask import Flask, jsonify, request
from flask import Blueprint
from common.baseResponseSingle import BaseResponseSingle
from models.kelas import Kelas
from schema.kelasSchema import KelasSchema
from services.kelasService import KelasService
from common.baseResponse import BaseResponse
from common.errorResponse import ErrorResponse
from app import db

ts = datetime.datetime.utcnow()

kelas_api = Blueprint('kelas_api', __name__)

@kelas_api.route("/kelas", methods=["GET"])
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
        kelas_schema = KelasSchema(many=True)
        data = KelasService.get_list(search, page, limit, sortBy) 
        print(kelas_schema.dump(data))
        return jsonify(
            BaseResponse(
                kelas_schema.dump(data),
                "Kelas successfully Show",
                page,
                limit,
                len(kelas_schema.dump(data)),
                200,
            ).serialize()
        ), 200

    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())

@kelas_api.route('/kelas', methods=["POST"]) 
def add_kelas():
    json = request.json

    kelas = json.get('kelas')

    try:
        add_kelas = Kelas(
            kelas = kelas,
            created_at=ts,
            updated_at=None,
            deleted_at=None
        )
        db.session.add(add_kelas)
        db.session.commit()

        return (
            jsonify(
                BaseResponseSingle(
                    kelas,
                    "Kelas successfully Add",
                    200,
                ).serialize()
            ),
            200
        )
    
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
@kelas_api.route('/kelas/<string:id>', methods=["GET"])
def get_by_id(id):
    try:
        data = KelasService.get_by_id(id) 
        if not data:
            return ErrorResponse(exception="Kelas is Not Found", code=400).serialize()
        kelas_schema = KelasSchema()
        return (
            jsonify(
                BaseResponseSingle(
                    kelas_schema.dump(data),
                    "Kelas successfully Showed",
                    200,
                ).serialize()
            ),
            200
        )
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
    
@kelas_api.route('/kelas/<string:id>', methods=["PUT"])
def update_kelas(id):

    kelas = request.json.get('kelas')
    try:
        data = KelasService.get_by_id(id)
        if not data or data.deleted_at is not None:
            return ErrorResponse(exception="Kelas is Not Found", code=400).serialize()

        data.kelas = kelas
        data.updated_at = ts
        db.session.commit()

        kelas_schema = KelasSchema() 

        return (
            jsonify(
                BaseResponseSingle(
                    kelas_schema.dump(data), 
                    "Kelas successfully Updated",
                    200,
                ).serialize()
            ),
            200
        )
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())



@kelas_api.route('/kelas/delete/<string:id>', methods=["PUT"])
def delete_kelas(id):
    
    try:
        data = KelasService.get_by_id(id)
        if data.deleted_at is not None:
            return ErrorResponse(exception="Kelas is Not Found", code=400).serialize()
        
        data.deleted_at = ts
        db.session.commit()

        return (
            jsonify(
                BaseResponseSingle(
                    data.id,
                    "Kelas successfully Deleted",
                    200,
                ).serialize()
            ),
            200
        )
    except Exception as e:
        traceback.print_exc()
        response = BaseResponse(None, str(e), 0, 0, 0, 400)
        return jsonify(response.serialize())
