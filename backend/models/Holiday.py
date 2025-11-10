from .db import db

class Holiday(db.Model):
    d_id = db.Column(db.Integer, db.ForeignKey("Doctors.d_id"), primary_key=True,nullable=False)
    date = db.Column(db.Date, primary_key=True,nullable=False)