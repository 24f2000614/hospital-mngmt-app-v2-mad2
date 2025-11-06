from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from api import Patients, Doctors

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("/patients", methods=['GET','POST'])
@admin_bp.route("/patients/<int:p_id>", methods=['GET','POST'])
@jwt_required()
def patient_handler(p_id=None):
    claims=get_jwt()
    if claims['role'] == "Admin":
        data = Patients().get(p_id)
        return data
    return jsonify({"message": "You are not authorized to access this route"})



@admin_bp.route("/doctors", methods=['GET','POST'])
@admin_bp.route("/doctors/<int:d_id>", methods=['GET','POST'])
@jwt_required()
def doctor_handler(d_id=None):
    claims=get_jwt()
    if claims['role'] == "Admin":
        if request.method == "GET":
            data = Doctor().get(d_id)
        elif request.method == "POST":
            if d_id == None:
                req = request.json
                result = Doctors().post(req)
                return result
            elif d_id:
                doctor = Doctor().get(d_id)
                
    return jsonify({"message": "You are not authorized to access this route"})


