from .db import db

class Appointment(db.Model):
    __tablename__ = "Appointments"
    a_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    p_id=db.Column(db.Integer, db.ForeignKey("Patients.p_id"),nullable=False)
    d_id=db.Column(db.Integer, db.ForeignKey("Doctors.d_id"),nullable=False)
    time=db.Column(db.DateTime, nullable=False)
    status=db.Column(db.String, nullable=False)
    prescription_id=db.Column(db.Integer, db.ForeignKey("Prescription.pr_id"))
    diagnosis=db.Column(db.String, nullable=True)