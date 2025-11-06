from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import Patient
from sqlalchemy.exc import IntegrityError

patient_fields = {
    "p_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "sex": fields.String,
    "phone_no": fields.String,
    "address": fields.String,
    "dob": fields.String
}

class Patients(Resource):
    def get(self, p_id=None):
        if p_id == None:
            items = Patient.query.all()
            data = [marshal(item, patient_fields) for item in items]
            return jsonify(data)