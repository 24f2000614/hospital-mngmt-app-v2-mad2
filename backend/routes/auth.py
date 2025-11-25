from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError
from models import db, Patient, Doctor, Admin, Blacklist
from datetime import date
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        email = request.json.get("email").lower()
        password = request.json.get("password")
    except:
        return jsonify({"message":"Invalid Input"})
            
    if db.session.get(Blacklist, email):
        return "This email is blacklisted"

    user = None
    id = None
    role = None

    patient = Patient.query.filter(Patient.email == email.lower()).first()
    if patient:
        user = patient
        id = patient.p_id
        role = "Patient"

    elif doctor := Doctor.query.filter(Doctor.email == email.lower()).first():
        user = doctor
        id = doctor.d_id
        role = "Doctor"

    elif admin := Admin.query.filter(Admin.email == email.lower()).first():
        user = admin
        id = admin.a_id
        role = "Admin"

    else:
        role = "None"

    if user and check_password_hash(user.password, password):
        additional_claims = {"role": role}
        access_token = create_access_token(identity=str(id), additional_claims= additional_claims)
        return jsonify(
            {
                "message": "Logged In!",
                "tokens": {
                    "access_token": access_token,
                }
            }
        )
    else:
        return jsonify({"message":"Incorrect Email or Password"})

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email=data['email'].lower()
    name=data['name']
    sex=data['sex']
    password=data['password']
    phone_no=str(data['phoneNum'])
    dob=list(map(int, data['dob'].split('-')))
    dob=date(dob[0], dob[1], dob[2])
    
    required_fields = ["email", "name", "sex", "password", "phoneNum", "dob"]
    missing = [f for f in required_fields if f not in data or not data[f]]

    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    if db.session.get(Blacklist, email):
        return "This email is blacklisted"

    if Patient.query.filter_by(phone_no=phone_no).first():
        return jsonify({"error": "Phone number is already registered"}), 409
    
    if Patient.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already registered"}), 409

    if len(phone_no) != 10:
        return jsonify({"error": "Phone number is not ten digits"})

    try:
        new_user=Patient(email=email,password=generate_password_hash(password),phone_no=phone_no,name=name, dob=dob, sex=sex)
        db.session.add(new_user)
        db.session.commit()
        return jsonify("Success")
    except IntegrityError as IE:
        db.session.rollback()
        return "Integrity Error"