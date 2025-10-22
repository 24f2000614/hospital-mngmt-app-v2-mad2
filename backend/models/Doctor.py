from .db import db

class Doctor(db.Model):
    __tablename__ = "Doctors"
    d_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False, unique=True)
    password=db.Column(db.String,nullable=False)
    description=db.Column(db.String, nullable=False, unique=True)
    dept_id=db.Column(db.Integer,db.ForeignKey("Departments.dept_id"),nullable=False)