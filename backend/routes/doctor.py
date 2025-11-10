from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from api import Holiday_Apis, Appointment_Apis, Patient_Apis

doctor_bp = Blueprint("doctor", __name__)

@doctor_bp.route('/appointments')
@doctor_bp.route('/appointments/<int:a_id>', methods=['GET', 'POST', 'DELETE'])
@jwt_required()
def appointment_handler(a_id = None):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return "You are not authorized to access this route"
    d_id = get_jwt_identity()
    if request.method == 'GET':
        if not a_id:
            appointments = Appointment_Apis().get(d_id=d_id)
        else: 
            appointments = Appointment_Apis().get(a_id=a_id)
            if appointments.d_id != d_id:
                return "You are not authorized to access this appointment"
        return appointments
    if request.method == 'POST':
        data = request.json
        diagnosis = data.get('diagnosis')
        prescription = data.get('prescription')
        result= Appointment_Apis().diagnosis(diagnosis)
        for p in prescription:
            for_result = Prescription_Apis().post(p)
        return result, for_result
    if request.method == 'DELETE':
        appointment = db.session.get(a_id)
        appointment.status = "Cancelled"
        db.session.commit()
        return "Success"
        
@doctor_bp.route('/history/<int:p_id>')
@jwt_required()
def history_handler(p_id):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return "You are not authorized to access this route"
    
    history = Patient_Apis().history(p_id)
    return history

@doctor_bp.route('/holiday/<int:d_id>', methods = ['GET', 'POST'])
@jwt_required()
def holiday_handler(d_id):
    claims = get_jwt()
    if claims['role'] != "Doctor":
        return "You are not authorized to access this route"
    d_id = get_jwt_identity()

    if request.method == 'GET':
        Holidays = Holiday_Apis().get(d_id)
        return Holidays
    elif request.method == 'POST':
        data = request.jsonify
        date = data.get('date')
        result = Holiday_Apis().book(d_id, date)
        return result

