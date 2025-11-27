from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Department
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

department_fields = {
    "dept_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
}

class Department_Apis(Resource):
    def get(self, dept_id=None):
        if dept_id:
            return marshal(db.session.get(Department,dept_id), department_fields)
        else:
            depts = Department.query.all()
            return [marshal(dept, department_fields) for dept in depts]

    def post(self, data):
        try:
            name = data.get("name")
            description = data.get("description")
            new_dept = Department(name=name, description=description)
            db.session.add(new_dept)
            db.session.commit()
            return "Success"
        except Error as e:
            db.session.rollback()
            return jsonify({"Error":e})

    def put(self, changes, dept_id):
        try:
            dept = db.session.get(Department, dept_id)
            for key,value in changes.items():
                if hasattr(dept, key) and "id" not in key:
                    setattr(dept, key, value)
            db.session.commit()
            return "Success"    
        except Error as e:
            db.session.rollback()
            return jsonify({"Error":e})

    def search(self, searchQ):
        search_by_name = Department.query.filter(Department.name.ilike(f"%{searchQ}%")).limit(5).all()
        return [marshal(item, department_fields) for item in search_by_name]


