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
    def get(self, pr_id=None):
        if not pr_id:
            prescriptions = Prescription.query.all()
            return [marshal(prescription,prescription_fields) for prescription in prescriptions]
        else:
            prescription = db.session.get(Prescription, pr_id)
            return marshal(prescription, prescription_fields)
        
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
