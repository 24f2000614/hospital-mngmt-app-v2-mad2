from .db import db

class Blacklist(db.Model):
    __tablename__ = "Blacklist",
    email = db.Column(db.String,primary_key=True, unique=True)