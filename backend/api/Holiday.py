from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Holiday
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

holiday_fields = {
    "d_id": fields.Integer,
    "date": fields.DateTime(dt_format='%d-%m-%Y'),
}

class Holiday_Apis(Resource):
    def get(self, d_id):
        Holidays = Holiday.query.filter(Holiday.d_id==d_id).all()
        return [marshal(holiday, holiday_fields) for holiday in Holidays]

    def book(self, d_id, date):
        try:
            Holiday = Holiday(d_id=d_id, date=date)
            db.session.add(Holiday)
            db.session.commit()
            return "Booked"
        except IntegrityError as E:
            return f"Integrity Error: {E}"