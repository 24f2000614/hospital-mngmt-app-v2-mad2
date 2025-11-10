from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Prescription
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

prescription_fields = {
    "pr_id": fields.Integer,
    "a_id": fields.Integer,
    "medicine": fields.String
}

class Prescription_Apis(Resource):
    def get(self, pr_id=None, a_id=None):
        if not pr_id and not a_id:
            prescriptions = Prescription.query.all()
            return [marshal(prescription,prescription_fields) for prescription in prescriptions]
        elif pr_id and not a_id:
            prescription = db.session.get(Prescription, pr_id)
            return marshal(prescription, prescription_fields)
        elif not pr_id and a_id:
            prescriptions = Prescription.query.filter(Prescription.a_id == a_id).all()
            return [marshal(prescription, prescription_fields) for prescription in prescriptions]
        else:
            return "Invalid Input params"
    def delete(self, pr_id=None):
        try:
            prescription = db.session.get(Prescription, pr_id)
            if prescription:
                db.session.delete(prescription)
                db.session.commit()
                return "Success"
            else:
                return "No prescription found"
        except IntegrityError:
            return "Integrity Error"
    def post(self, data):
        a_id=data.get("a_id")
        medecine = data.get("medicine")
        prescription = Prescription(a_id=a_id, medicine=medecine)
        db.session.add(prescription)
        db.session.commit()