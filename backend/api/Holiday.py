from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Holiday, Appointment
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from sqlalchemy import func

holiday_fields = {
    "d_id": fields.Integer,
    "date": fields.DateTime(dt_format='%Y-%m-%d'),
}

class Holiday_Apis(Resource):
    def get(self, d_id):
        Holidays = Holiday.query.filter(Holiday.d_id==d_id).all()
        return [marshal(holiday, holiday_fields) for holiday in Holidays]

    def isAvailable(self, date, d_id):
        HolidayMatch = Holiday.query.filter(
            Holiday.d_id == d_id,
            Holiday.date == date
        ).first()
        if HolidayMatch:
            return False
        return True

    def book(self, d_id, date):
        try:
            getApp = Appointment.query.filter(
                Appointment.d_id == d_id, 
                func.date(Appointment.start_time) == date    
            )
            if getApp:
                return jsonify({"message": "You have scheduled appointments on this day!"})
            Holiday = Holiday(d_id=d_id, date=date)
            db.session.add(Holiday)
            db.session.commit()
            return "Booked"
        except IntegrityError as E:
            return f"Integrity Error: {E}"