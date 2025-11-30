from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from api import Appointment_Apis, Department_Apis, Doctor_Apis, Prescription_Apis, Patient_Apis, Holiday_Apis
from datetime import datetime, date, timedelta, time

def get_dates():
    today = date.today()
    next_week_dates = []
    for i in range(1, 8):
        day = today + timedelta(days=i)
        strday = day.strftime('%A %d-%m-%Y')
        next_week_dates.append(strday)

    return next_week_dates


patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/appointments", methods=['GET','POST'])
@patient_bp.route("/appointments/<int:a_id>", methods=['GET','PUT', 'DELETE'])
@jwt_required()
def appointment_handler(a_id=None):
    claims= get_jwt()
    if claims['role'] != "Patient":
        return jsonify({"message": "You are not authorized to access this route"}), 403
    p_id = int(get_jwt_identity())

    if request.method == 'GET':
        if not a_id:
            appointments = Appointment_Apis().get(p_id=p_id)
            return appointments
        else: 
            appointment =Appointment_Apis().get(p_id = p_id, a_id=a_id)
            prescription = Prescription_Apis().get(a_id=a_id)
            return jsonify({"appointment": appointment, "prescription": prescription})
    elif request.method == "POST":
        data = request.json
        p_id = int(get_jwt_identity())
        data["p_id"] = p_id
        result = Appointment_Apis().post(data)
        return result

    elif request.method == "PUT":
        data = request.json
        new_start = data.get('start_time')
        if data.get("p_id") == p_id:
            result = Appointment_Apis().reschedule(new_start,a_id)
            return result
        else:
            return jsonify({"message": "You are not authorized to access this route"}), 401
    elif request.method == "DELETE":
        appointment = Appointment_Apis().get(a_id=a_id)
        if appointment.get("p_id") == p_id:
            result = Appointment_Apis().delete(a_id=a_id)
            return result
        else:
            return jsonify({"message": "You are not authorized to access this route"}), 401

@patient_bp.route("/search-doctor", methods=['POST'])
@jwt_required()
def doc_search_handler():
    claims = get_jwt()
    if claims['role'] != 'Patient':
        return jsonify({"message":"You are not authorized to access this route"}),403

    searchQ = request.json.get("searchQ")
    dept_id = request.json.get("dept_id")
    if not dept_id:
        response = Doctor_Apis().search(searchQ)
    elif dept_id:
        response = Doctor_Apis().search(searchQ, d_id=dept_id)
    return response

@patient_bp.route("/search-dept", methods=['POST'])
@jwt_required()
def dept_search_handler():
    claims = get_jwt()
    if claims['role'] != 'Patient':
        return jsonify({"message":"You are not authorized to access this route"}),403
    searchQ = request.json.get("searchQ")
    results = Department_Apis().search(searchQ)
    return results

@patient_bp.route('/dept', methods=['GET'])
@patient_bp.route('/dept/<int:dept_id>', methods=['GET'])
@jwt_required()
def get_depts(dept_id=None):
    claims = get_jwt()
    if claims['role'] != 'Patient':
        return jsonify({"message":"You are not authorized to access this route"}),403

    if dept_id:
        dept_info = Department_Apis().get(dept_id)
        doctor_info = Doctor_Apis().get(dept_id=dept_id)
        return jsonify({"dept": dept_info, "doctor_list":doctor_info})
    else:
        return Department_Apis().get()

@patient_bp.route('/profile/<int:p_id>', methods=['GET', "PUT"])
@jwt_required()
def profile_handler(p_id):
    claims=get_jwt()
    if p_id == int(get_jwt_identity()):
        if claims['role'] == "Patient" and p_id:
            if request.method == "GET":
                patient = Patient_Apis().get(p_id)
                return patient
            elif request.method == "PUT":
                changes = request.json
                result = Patient_Apis().put(changes, p_id)
                return result

@patient_bp.route('/doc-availability/<int:d_id>', methods = ['GET'])
@jwt_required()
def availability(d_id):
    dates = get_dates()
    availability = []
    for day in dates:
        slots = [[i, True] for i in range(9,23)]
        date = datetime.strptime(day, '%A %d-%m-%Y').date()
        is_free = Holiday_Apis().isAvailable(date=date, d_id=d_id)
        item = {
            "date": day,
            "available": is_free,
            "slots": slots
        }
        if is_free:
            appointments = Appointment_Apis().get(date=date, d_id= d_id, status='Booked')
            for slot in slots:
                for appointment in appointments:
                    dateobj = datetime.strptime(appointment['start_time'], "%a, %d %b %Y %H:%M:%S %z")
                    if slot[0] == dateobj.hour:
                        slot[1] = False
        availability.append(item)
    return availability

@patient_bp.route('/doctor-info/<int:d_id>', methods = ['GET'])
@jwt_required()
def doc_info(d_id):
    data = Doctor_Apis().get(d_id)
    return data