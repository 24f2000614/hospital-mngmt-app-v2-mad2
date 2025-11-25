from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from api import Appointment_Apis, Department_Apis, Doctor_Apis, Prescription_Apis

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/appointments", methods=['GET','POST'])
@patient_bp.route("/appointments/<int:a_id>", methods=['GET','PUT', 'DELETE'])
@jwt_required()
def appointment_handler(a_id=None):
    claims= get_jwt()
    if claims['role'] != "Patient":
        return jsonify({"message": "You are not authorized to access this route"})
    p_id = int(get_jwt_identity())

    if request.method == 'GET':
        if not a_id:
            appointments = Appointment_Apis().get(p_id=p_id)
            return appointments
        else: 
            appointment =Appointment_Apis().get(p_id = p_id, a_id=a_id)
            prescription = Prescription_Apis().get(a_id=a_id)
    elif request.method == "POST":
        data = request.json
        if data.get("p_id") == p_id:
            result = Appointment_Apis().post(data)
            return result
        else:
            return "You're not authorized to book appointments for this user"
    elif request.method == "PUT":
        data = request.json
        new_start = data.get('time')
        duration = data.get('duration')
        if data.get("p_id") == p_id:
            result = Appointment_Apis().reschedule(new_start, duration,a_id)
            return result
        else:
            return "You're not authorized to reschedule appointments for this user"
    elif request.method == "DELETE":
        # appointment = db.session.get(Appointment, a_id)
        appointment = Appointment_Apis().get(a_id=a_id)
        if appointment.get("p_id") == p_id:
            result = Appointment_Apis().delete(a_id=a_id)
            return result
        else:
            return "You're not authorized to cancel appointments for this user"

@patient_bp.route("/search-doctor", methods=['GET'])
@jwt_required()
def search_handler():
    claims = get_jwt()
    if claims['role'] != 'Patient':
        return "You are not authorized to access this route"
    searchQ = request.json.get("searchQ")
    dept_id = request.json.get("dept_id")
    if not dept_id:
        response = Doctor_Apis().search(searchQ)
    elif dept_id:
        response = Doctor_Apis().search(searchQ, d_id=dept_id)
    return response

@patient_bp.route('/dept', methods=['GET'])
@patient_bp.route('/dept/<int:dept_id>', methods=['GET'])
@jwt_required()
def get_depts(dept_id=None):
    claims = get_jwt()
    if claims['role'] != 'Patient':
        return "You are not authorized to access this route"
    if dept_id:
        dept_info = Department_Apis().get(dept_id)
        doctor_info = Doctor_Apis().get(dept_id=dept_id)
        return jsonify({"dept": dept_info, "doctor_info":doctor_info})
    else:
        return Department_Apis().get()

@patient_bp.route('/profile', methods=['GET', "PUT"])
@jwt_required()
def profile_handler():
    claims=get_jwt()
    p_id=int(get_jwt_identity())
    if claims['role'] == "Patient" and p_id:
        if request.method == "GET":
            patient = Patient_Apis().get(p_id)
            return patient
        elif request.method == "PUT":
            changes = request.json
            result = Patient_Apis().put(changes, p_id)
            return result