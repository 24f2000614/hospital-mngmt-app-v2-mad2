from .db import db

class Admin(db.Model):
    __tablename__ = "Admin"
    a_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    