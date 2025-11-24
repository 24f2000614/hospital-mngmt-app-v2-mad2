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
    def get(self,a_id=None):
        prescriptions = Prescription.query.filter(Prescription.a_id == a_id).all()
        return [marshal(prescription, prescription_fields) for prescription in prescriptions]
        
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
    def post(self, medicine, a_id):
        prescription = Prescription(a_id=a_id, medicine=medicine)
        db.session.add(prescription)
        db.session.commit()