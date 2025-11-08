from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import Patient, Blacklist
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
