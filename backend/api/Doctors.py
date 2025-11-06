from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Doctor
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

doctor_fields = {
    "d_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "description": fields.String,
    "dept_id": fields.Integer,
}

class Doctors(Resource):
    def get(self, d_id=None):
        if d_id == None:
            items = Doctor.query.all()
            data = [marshal(item, doctor_fields) for item in items]
            return jsonify(data)
        elif type(d_id) == int:
            item = Doctor.query.filter(Doctor.d_id == d_id).first()
            data = marshal(item, doctor_fields)
            return jsonify(data)
    
    def post(self, data):
        name=data["name"]
        email=data["email"]
        password="doctor123"
        description=data['description']
        dept_id=int(data['dept_id'])
        try:
            new_doc=Doctor(email=email,password=generate_password_hash(password),name=name, dept_id=dept_id, description=description)
            db.session.add(new_doc)
            db.session.commit()
            return jsonify("Success")
        except IntegrityError:
            db.session.rollback()
            return jsonify("Integrity Error")