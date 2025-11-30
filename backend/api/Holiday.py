from flask import jsonify
from flask_restful import Resource, fields, marshal
from models import db, Holiday, Appointment
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from sqlalchemy import func

holiday_fields = {
    "d_id": fields.Integer,
    "date": fields.DateTime(dt_format='iso8601'),
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
            date = datetime.strptime(date, '%A %d-%m-%Y')
            getApp = Appointment.query.filter(
                Appointment.d_id == d_id, 
                func.date(Appointment.start_time) == date,
                Appointment.status == 'Booked'  
            ).first()
            if getApp:
                return jsonify({"message": "You have scheduled appointments on this day!"}), 401
            Day = Holiday(d_id=d_id, date=date)
            db.session.add(Day)
            db.session.commit()
            return "Booked", 200
        except IntegrityError as E:
            return f"Integrity Error: {E}"