from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Doctor
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
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
            return jsonify({"message":str(e)}), 400

        if dept_id is not None:
            items = Doctor.query.filter_by(dept_id=dept_id).all()
            return [marshal(item, doctor_fields) for item in items]

        if d_id is not None:
            item = db.session.get(Doctor, d_id)
            if not item:
                return jsonify({"message":str(e)}), 400
            return marshal(item, doctor_fields)

        items = Doctor.query.all()
        return [marshal(item, doctor_fields) for item in items]

    def post(self, data):
        try:
            name=data.get("name")
            email=data.get("email").lower()
            password="doctor123"
            description=data.get("description")
            dept_id=int(data.get("dept_id"))
            new_doc=Doctor(email=email,password=generate_password_hash(password),name=name, dept_id=dept_id, description=description)
            db.session.add(new_doc)
            db.session.commit()
            return "Success"
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    def put(self, changes, d_id):
        try:
            doctor = db.session.get(Doctor, d_id)
            if not doctor:
                return {"message": "Doctor not found"}, 404
            for key, value in changes.items():
                if hasattr(doctor, key) and "id" not in key:
                    if key == "password":
                        setattr(doctor, key, generate_password_hash(value))
                    else:
                        setattr(doctor, key, value)
            db.session.commit()
            return "Success"
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":str(e)}), 400

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
        except Exception as e:
            return jsonify({"message":str(e)}), 400

    def search(self, searchQ, d_id= None):
        if not d_id:
            results = Doctor.query.filter(
                or_(
                    Doctor.name.ilike(f"%{searchQ}%"),
                    Doctor.email.ilike(f"%{searchQ}%")
                    )
                ).limit(5).all()
        else:
            results = Doctor.query.filter(Doctor.name.ilike(f"%{searchQ}%"), Doctor.dept_id == d_id).limit(5).all()

        return [marshal(search_item, doctor_fields) for search_item in results]
