from .db import db

class Prescription(db.Model):
    __tablename__ = "Prescription"
    pr_id=db.Column(db.Integer, primary_key=True,nullable=False)
    a_id=db.Column(db.Integer, db.ForeignKey("Appointments.a_id"),nullable=False)
    medicine= db.Column(db.String, nullable=False)