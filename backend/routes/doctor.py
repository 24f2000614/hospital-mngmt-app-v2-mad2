from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from api import Holiday_Apis, Appointment_Apis, Patient_Apis, Prescription_Apis, Doctor_Apis

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route('/appointments')
@doctor_bp.route('/appointments/<int:a_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def appointment_handler(a_id = None):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return jsonify({"message":"You are not authorized to access this route"}),403
    d_id = int(get_jwt_identity())
    if request.method == 'GET':
        if not a_id:
            appointments = Appointment_Apis().get(d_id=d_id)
            return appointments
        else: 
            appointment = Appointment_Apis().get(a_id=a_id)
            if appointment.get("d_id")!= d_id:
                return jsonify({"message":"You are not authorized to access this route"}),403
            prescriptions = Prescription_Apis().get(a_id=a_id)
            return jsonify({"appointment": appointment, "prescriptions": prescriptions})
    if request.method == 'POST':
        data = request.json
        diagnosis = data.get('diagnosis')
        # prescription = data.get('prescriptions')
        result= Appointment_Apis().diagnosis(diagnosis=diagnosis, a_id=a_id)
        return result
    if request.method == 'PUT':
        result = Appointment_Apis().complete(a_id)
        return result
    if request.method == 'DELETE':
        # appointment = Appointment_Apis().get(a_id=a_id)
        result = Appointment_Apis().cancel(a_id=a_id)
        return result
        
@doctor_bp.route('/history/<int:p_id>')
@jwt_required()
def history_handler(p_id):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return jsonify({"message":"You are not authorized to access this route"}),403
    
    history = Patient_Apis().history(p_id)
    return history

@doctor_bp.route('/holiday/<int:d_id>', methods = ['GET', 'POST'])
@jwt_required()
def holiday_handler(d_id):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return jsonify({"message":"You are not authorized to access this route"}),403
    d_id = int(get_jwt_identity())

    if request.method == 'GET':
        Holidays = Holiday_Apis().get(d_id)
        return Holidays
    elif request.method == 'POST':
        data = request.json
        date = data.get('date')
        result = Holiday_Apis().book(d_id, date)
        return result

@doctor_bp.route('/patient-info', methods = ['GET'])
@doctor_bp.route('/patient-info/<int:p_id>', methods = ['GET'])
@jwt_required()
def patient_info(p_id= None):
    if p_id:
        data = Patient_Apis().get(p_id)
        return data

@doctor_bp.route('/profile/<int:d_id>', methods=['GET'])
@jwt_required()
def profile_handler(d_id):
    claims=get_jwt()
    if d_id == int(get_jwt_identity()):
        if claims['role'] == "Doctor" and d_id:
            doctor = Doctor_Apis().get(d_id)
            return doctor

@doctor_bp.route('/prescription', methods=['POST'])
@doctor_bp.route('/prescription/<int:pr_id>', methods=['DELETE'])
@jwt_required()
def prescription(pr_id=None):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return jsonify({"message":"You are not authorized to access this route"}),403
    if request.method == 'DELETE':
        result = Prescription_Apis().delete(pr_id)
        return result
    if request.method == 'POST':
        data = request.json
        prescription = data.get('medicine')
        a_id = data.get('a_id')
        result = Prescription_Apis().post(prescription=prescription, a_id= a_id)
        return result