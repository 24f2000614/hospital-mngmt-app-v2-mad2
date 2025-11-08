from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Appointment
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from .Prescription import Prescription_Apis

appointment_fields = {
    "a_id": fields.Integer,
    "p_id": fields.Integer,
    "d_id": fields.Integer,
    "start_time": fields.DateTime,
    "end_time": fields.DateTime,
    "status": fields.String,
    "prescription": fields.Integer
}

class Appointment_Apis(Resource):
    def get(self, a_id=None):
        if not a_id:
            appointments = Appointment.query.all()
            return jsonify([marshal(appointment, appointment_fields) for appointment in appointments])
        else:
            appointment = db.session.get(Appointment, a_id)
            return jsonify(marshal(appointment, appointment_fields))
        
    def post(self, data):
        p_id= data["p_id"]
        d_id= data["d_id"]
        start_time= data["start"]
        end_time= data["end"]
        status= data["status"]
        prescription= data["pr_id"]

        try:
            new_appoint = Appointment(p_id=p_id,d_id=d_id,start_time=start_time,end_time=end_time,status=status,prescription=prescription)
            db.session.add(new_appoint)
            db.session.commit()
            return "Success"
        except IntegrityError:
            db.session.rollback()
            return "Integrity Error"

    def reschedule(self, new_start, a_id):
        try:
            appointment = db.session.get(Appointment, a_id)
            if appointment.status == "Scheduled":
                appointment.start_time = new_start
                db.session.commit()
                return "Success"
            else:
                return "Cannot edit time of this appointment"
        except IntegrityError:
            db.session.rollback()
            return "IntegrityError"

    def cancel(self, a_id=None, d_id=None):
        try:
            if a_id and not d_id:
                appointment = db.session.get(Appointment,a_id)
                if appointment is not None:
                    db.session.delete(appointment)
                    db.session.commit()
                    return "Success"
                else:
                    return f"No appointment found with id={a_id}"
            elif d_id and not a_id:
                appointments = Appointment.query.filter(Appointment.d_id==d_id).all()
                if appointments:
                    for appointment in appointments:
                        Prescription_Apis().delete(a_id=appointment.a_id)
                        db.session.delete(appointment)
                    db.session.commit()
                    return "Success"
                else:
                    return f"No appointments found for doctor id={d_id}"
            else:
                return "Invalid input"
        except IntegrityError:
            db.session.rollback()
            return "Integrity Error"
