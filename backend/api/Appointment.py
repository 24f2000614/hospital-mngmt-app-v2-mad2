from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Appointment
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from .Prescription import Prescription_Apis
from .Holiday import Holiday_Apis
from datetime import datetime, timedelta, time

appointment_fields = {
    "a_id": fields.Integer,
    "p_id": fields.Integer,
    "d_id": fields.Integer,
    "start_time": fields.DateTime,
    "end_time": fields.DateTime,
    "status": fields.String,
    "prescription": fields.Integer(default=None),
    "diagnosis": fields.String
}

def Rules_and_conflict(start_time, duration, d_id):
    if start_time.date() <= datetime.now().date():
        return "Appointments need to be booked at least one day before" 

    if (start_time.date() - datetime.now().date()) > timedelta(days=180):
        return "Appointments need to be booked within 6 months or 180 days from today"
    
    Doctors_off = Holiday_Apis().get(d_id)
    for day in Doctors_off:
        if start_time.date() == day['date']:
            doctor = db.session.get(Doctor, d_id)
            name = doctor.name
            return f"Dr. {name} is unavailable for this date"

    if start_time.time() < time(9,0) or start_time.time() > time(22, 0):
        return "Appointments need to be booked during office hours only 9-6"

    if duration > 60:
        return "Appointments cannot be booked for more than an hour"
    
    if start_time.minute % 15 != 0 or start_time.second != 0:
        return "You can only book an appointment every 15 minutes"    

    date = start_time.date()
    end_time = start_time + timedelta(minutes=duration)
    appointments = Appointment.query.filter(
        func.date(Appointment.start_time) == date, 
        Appointment.d_id == d_id,
        Appointment.status == 'Booked'
    ).all()

    for appointment in appointments:
        start = appointment.start_time 
        end = appointment.end_time
        if start < end_time and start_time < end:
            return "The Doctor is unavailable during this time slot"
    return "OK"

class Appointment_Apis(Resource):
    def get(self, a_id=None, p_id = None, d_id=None):
        if not a_id and not p_id and not d_id:
            appointments = Appointment.query.all()
            return [marshal(appointment, appointment_fields) for appointment in appointments]
        elif a_id and not p_id and not d_id:
            appointment = db.session.get(Appointment, a_id)
            return marshal(appointment, appointment_fields)
        elif not a_id and p_id and not d_id:
            appointments = Appointment.query.filter(Appointment.p_id == p_id).all()
            return [marshal(appointment, appointment_fields) for appointment in appointments]
        elif not a_id and not p_id and d_id:
            appointments = Appointment.query.filter(Appointment.d_id == d_id).all()
            return [marshal(appointment, appointment_fields) for appointment in appointments]
        elif a_id and p_id and not d_id:
            appointments = Appointment.query.filter(Appointment.p_id == p_id, Appointment.a_id == a_id).all()
            return [marshal(appointment, appointment_fields) for appointment in appointments]
        else:
            return "Invalid params"
             
    def post(self, data):
        p_id= data.get("p_id")
        d_id= data.get("d_id")
        start_time= datetime.fromisoformat(data["start"])
        duration = data.get("duration")
        end_time = start_time + timedelta(minutes = data["duration"])
        status= data["status"]
        prescription= data.get('pr_id')

        conflict_check = Rules_and_conflict(start_time, duration, d_id)
        if conflict_check != "OK":
            return conflict_check
        try:
            new_appoint = Appointment(p_id=p_id,d_id=d_id,start_time=start_time,end_time=end_time,status=status,pr_id=prescription)
            db.session.add(new_appoint)
            db.session.commit()
            return "Success"
        except IntegrityError:
            db.session.rollback()
            return "Integrity Error"

    def reschedule(self, new_start, duration, a_id):
        try:
            appointment = db.session.get(Appointment, a_id)
            new_start = datetime.fromisoformat(new_start)
            
            conflict_check = Rules_and_conflict(start_time, duration, d_id)
            if conflict_check != "OK":
                return conflict_check
            
            if appointment.status == "Booked":
                appointment.start_time = new_start
                appointment.end_time = new_start + timedelta(minutes=duration)
                db.session.commit()
                rescheduled = marshal(db.session.get(Appointment, a_id), appointment_fields)
                return jsonify({"message": "Success", "rescheduled": rescheduled })
            else:
                return "Cannot edit time of this appointment"
        except IntegrityError:
            db.session.rollback()
            return "IntegrityError"

    def delete(self, a_id=None):
        try:
            appointment = db.session.get(Appointment,a_id)
            if appointment is not None:
                if appointment.status != 'Completed':
                    db.session.delete(appointment)
                    db.session.commit()
                    return "Success"
                else:
                    return "This appointment is completed and cannot be deleted."
            else:
                return f"No appointment found with id={a_id}"
        except IntegrityError:
            db.session.rollback()
            return "Integrity Error"

    def cancel(self, a_id=None, d_id=None):
        if a_id and not d_id:
            appointment = db.session.get(Appointment, a_id)
            appointment.status = "Cancelled"

    def started(self, a_id):
        appointment = db.session.get(Appointment,a_id)
        now = datetime.now()
        if now < appointment.start_time:
            return False
        return True
        


    def diagnosis(self, a_id, diagnosis):
        appointment = db.session.get(Appointment,a_id)
        now = datetime.now()
        if not appointment:
            return "Appointment doesnt exist"
        if now < appointment.start_time:
            return "The appointment is yet to start"
        appointment.diagnosis = diagnosis
        appointment.status = "Completed"
        db.session.commit()
        return "Success"