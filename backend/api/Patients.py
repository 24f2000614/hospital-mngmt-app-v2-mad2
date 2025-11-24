from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import Patient, Blacklist
from .Appointment import Appointment_Apis, Prescription_Apis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only

patient_fields = {
    "p_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "sex": fields.String,
    "phone_no": fields.String,
    "address": fields.String,
    "dob": fields.String
}

class Patient_Apis(Resource):
    def get(self, p_id=None):
        if p_id == None:
            items = Patient.query.all()
            data = [marshal(item, patient_fields) for item in items]
            return data
        else:
            try:
                item = Patient.query.filter(p_id == p_id).first()
                data = marshal(item, patient_fields)
                return data
            except:
                return jsonify("Error")
    
    def blacklist(self, p_id):
        try:
            patient = db.session.get(Patient, p_id)
            if not patient:
                return "No patient found"
            b_listed_item = Blacklist(email = patient.email, phone_no= patient.phone_no)
            db.session.add(b_listed_item)
            db.session.delete(patient)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            return "Integrity Error"

    def search(self, searchQ):
        if searchQ.isdigit():
            search_by_num = Patient.query.filter(
                _or(
                    Patient.p_id.ilike(f"%{searchQ}%"),
                    Patient.phone_no.ilike(f"%{searchQ}%")
                )
                ).limit(5).all()
            return [marshal(search_item, patient_fields) for search_item in search_by_num]
        else:
            search_by_name = Patient.query.filter(Patient.name.ilike(f"%{searchQ}%")).limit(5).all()
            return [marshal(search_item, patient_fields) for search_item in search_by_name]

    def history(self, p_id):
        history = {}
        appointments = Appointment_Apis().get(p_id=p_id)
        for appointment in appointments:
            history[appointment["a_id"]] = {
                "appointment": appointment,
                "prescriptions": Prescription_Apis().get(appointment["a_id"])
            }
        return history

    def put(self, changes, p_id):
        try:
            patient = db.session.get(p_id)
            for key, value in changes.items():
                if hasattr(patient, key) and "id" not in key:
                    setattr(patient, key, value)
            db.session.commit()
            return "Success"
        except Error as e:
            db.session.rollback()
            return jsonify({"Error":e})