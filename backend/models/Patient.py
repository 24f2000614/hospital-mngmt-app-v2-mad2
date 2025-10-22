from .db import db

class Patient(db.Model):
    __tablename__ = "Patients"
    p_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False, unique=True)
    password=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.Integer, nullable=False, unique=True)
    address=db.Column(db.String, nullable=True)