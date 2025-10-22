from .db import db

class Department(db.Model):
    __tablename__ = "Departments"
    dept_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)