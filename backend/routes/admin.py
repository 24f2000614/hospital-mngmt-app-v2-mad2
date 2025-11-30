from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from flask_cors import cross_origin
from api import Patient_Apis, Doctor_Apis, Appointment_Apis, Department_Apis, Prescription_Apis, Blacklist_Apis

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("/patients")
@admin_bp.route("/patients/<int:p_id>", methods = ["GET", "DELETE", "PUT"])
@jwt_required()
def patient_handler(p_id=None):
    claims=get_jwt()
    if claims['role'] == "Admin":
        if request.method == "GET":
            data = Patient_Apis().get(p_id)
            return data
        elif request.method == "DELETE": 
            if p_id:
                Patient_Apis().blacklist(p_id)
                return "Success"
            else:
                return "Missing patient id"
        elif request.method == "PUT":
            if p_id:
                changes = request.json
                result = Patient_Apis().put(changes, p_id)
                return result
            else: 
                return "Missing patient id"
    return jsonify({"message": "You are not authorized to access this route"}), 403

@admin_bp.route("/history/<int:a_id>")
@jwt_required()
def history_handler(a_id):
    appointment = dict(Appointment_Apis().get(a_id=a_id))
    prescriptions = Prescription_Apis().get(a_id=a_id)
    patient = Patient_Apis().get(p_id=appointment['p_id'])
    doctor = Doctor_Apis().get(d_id=appointment['d_id'])
    return jsonify({"appointment": appointment, "prescriptions": prescriptions, "doctor": doctor, "patient": patient})

@admin_bp.route("/doctors", methods=['GET','POST'])
@admin_bp.route("/doctors/<int:d_id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def doctor_handler(d_id=None):
    claims=get_jwt()
    if claims["role"] == "Admin":
        if request.method == "GET":
            data = Doctor_Apis().get(d_id)
            return data
        elif request.method == "POST":
            req = request.json
            result = Doctor_Apis().post(req)
            return result
        elif request.method == "PUT":
            changes = request.json
            result = Doctor_Apis().put(changes=changes, d_id=d_id)
            return result
        elif request.method == "DELETE":
            if d_id:
                result = Doctor_Apis().delete(d_id)
                return jsonify(result)
            else:
                return "Deleting requires specific ID"
    return jsonify({"message": "You are not authorized to access this route"}), 403

@admin_bp.route("/appointments", methods=['GET'])
@admin_bp.route("/appointments/<int:a_id>", methods=['GET','DELETE'])
@jwt_required()
def appointment_handler(a_id=None):
    claims = get_jwt()
    if claims["role"] == "Admin":
        if request.method == "GET":
            if a_id:
                appointment = Appointment_Apis().get(a_id=a_id)
                return appointment
            else:
                appointments = Appointment_Apis().get()
                return appointments
        elif request.method == "DELETE":
            result = Appointment_Apis().cancel(a_id)
            return result
    else:
        return jsonify({"message": "You are not authorized to access this route"}), 403

@admin_bp.route("/search/<srch_type>", methods=['POST'])
@jwt_required()
def search_handler(srch_type):
    claims= get_jwt()
    if claims["role"] == "Admin":
        if srch_type in ["doctors", "patients", "departments"]:
            searchQ = request.json.get("searchQ")
            if srch_type == "doctors":
                results = Doctor_Apis().search(searchQ)
            elif srch_type == "patients":
                results = Patient_Apis().search(searchQ)
            elif srch_type == "departments":
                results = Department_Apis().search(searchQ)
            return results
        else:
            return "Not a valid search"
    else:
        return jsonify({"message": "You are not authorized to access this route"}), 403

@admin_bp.route("/dept", methods=['GET', 'POST'])
@admin_bp.route("/dept/<int:dept_id>", methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def department_handler(dept_id = None):
    claims = get_jwt()    
    if request.method == 'GET':
        dept = Department_Apis().get(dept_id)
        return dept
    if claims['role'] != "Admin":
        return jsonify({"message":"You are not authorized to access this route"}),403
    if request.method == 'POST':
        data = request.json
        result = Department_Apis().post(data)
        return result
    elif request.method == 'PUT':
        changes = request.json
        result = Department_Apis().put(changes, dept_id)
        return result
    elif request.method == 'DELETE':
        changes = request.json
        result = Department_Apis().put(changes, dept_id)
        return result

@admin_bp.route("/blacklist")
@jwt_required()
def get_blacklist():
    claims = get_jwt()
    if claims['role'] != "Admin":
        return jsonify({"message":"You are not authorized to access this route"}),403
    
    blacklist = Blacklist_Apis().get()
    return blacklist
    
