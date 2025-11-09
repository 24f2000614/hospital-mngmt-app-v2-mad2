from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Doctor
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from .Appointment import Appointment_Apis

doctor_fields = {
    "d_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "description": fields.String,
    "dept_id": fields.Integer,
}

class Doctor_Apis(Resource):
    def get(self, d_id=None, dept_id= None):
        if d_id and dept_id:
            return "Only one param at a time!"
        if d_id == None:
            items = Doctor.query.all()
            data = [marshal(item, doctor_fields) for item in items]
            return jsonify(data)
        elif type(d_id) == int:
            item = db.session.get(Doctor, d_id)
            data = marshal(item, doctor_fields)
            return jsonify(data)
        elif dept_id:
            items = Doctor.query.filter(Doctor.dept_id == dept_id).all()
            data = [marshal(item, doctor_fields) for item in items]
            return jsonify(data)

    def post(self, data):
        try:
            name=data.get("name")
            email=data.get("email")
            password="doctor123"
            description=data.get("description")
            dept_id=int(data.get("dept_id"))
            new_doc=Doctor(email=email,password=generate_password_hash(password),name=name, dept_id=dept_id, description=description)
            db.session.add(new_doc)
            db.session.commit()
            return "Success"
        except Error as e:
            db.session.rollback()
            return jsonify({"Error":e})
    
    def put(self, changes, d_id):
        try:
            doctor = db.session.get(Doctor, d_id)
            if not doctor:
                return {"message": "Doctor not found"}, 404
            for key, value in changes.items():
                if hasattr(doctor, key) and "id" not in key:
                    setattr(doctor, key, value)
            db.session.commit()
            return "Success"
        except Error as e:
            db.session.rollback()
            return jsonify({"Error":e})

    def delete(self,d_id):
        try:
            doctor = db.session.get(Doctor, d_id)
            appointments = Appointment_Apis().cancel(d_id=d_id)
            if doctor:
                db.session.delete(doctor)
            else:
                return "Doctor does not exist"
            db.session.commit()
            return "Success"
        except IntegrityError:
            return "Integrity Error"
    
    def search(self, searchQ, d_id= None):
        if not d_id:
            results = Doctor.query.filter(Doctor.name.ilike(f"%{searchQ}%")).limit(5).all()
        else:
            results = Doctor.query.filter(Doctor.name.ilike(f"%{searchQ}%"), Doctor.dept_id == d_id).limit(5).all()

        return [marshal(search_item, doctor_fields) for search_item in results]