from flask_restful import Resource, fields, marshal
from models import db, Patient, Doctor, Appointment, Prescription
from sqlalchemy import func
import datetime

appointment_fields = {
    "a_id": fields.Integer,
    "p_id": fields.Integer,
    "d_id": fields.Integer,
    "start_time": fields.DateTime,
    "end_time": fields.DateTime,
    "status": fields.String,
    "diagnosis": fields.String
}
patient_fields = {
    "p_id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "sex": fields.String,
    "phone_no": fields.String,
    "address": fields.String,
    "dob": fields.String
}
prescription_fields = {
    "pr_id": fields.Integer,
    "a_id": fields.Integer,
    "medicine": fields.String
}


class Backend_Apis(Resource):
    def daily_reminders(self, date):
        response = []
        Appquery = Appointment.query.filter(
            func.date(Appointment.start_time) == date,
            Appointment.status == 'Booked'
        )
        appointments = list(Appquery)
        for appointment in appointments:
            item = {"email": None, "p_name": None, "slot": appointment.start_time.hour, "d_name": None}
            p_id = appointment.p_id
            d_id = appointment.d_id
            patient = db.session.get(Patient, p_id)
            doctor = db.session.get(Doctor, d_id)
            item["email"] = patient.email
            item["p_name"] = patient.name
            item["d_name"] = doctor.name
            response.append(item)
        return response

    def monthly_report(self, start, end, d_id):
        response = []
        appointments = Appointment.query.filter(
            Appointment.d_id == d_id,
            func.date(Appointment.start_time) <= end,
            func.date(Appointment.start_time) >= start, 
        ).all()
        for a in appointments:
            a_id = a.a_id
            p_id = a.p_id
                
            prescQ = Prescription.query.filter(Prescription.a_id == a_id).all()
            patQ = db.session.get(Patient, p_id)
            patient = marshal(patQ, patient_fields)
            prescriptions =  [marshal(prescription, prescription_fields) for prescription in prescQ]                
            dateObj = a.start_time
            appointment = marshal(a, appointment_fields)
            date = f"{dateObj.day}-{dateObj.month}-{dateObj.year}"
            slot = dateObj.hour
            response.append({"appointment": appointment, "prescriptions": prescriptions, "patient": patient, "date": date, "slot": slot})
        return response

    def csv_data(self, p_id):
        response = []
        patientQuery = db.session.get(Patient, p_id)
        patient = marshal(patientQuery, patient_fields)
        appointments = list(Appointment.query.filter(
            Appointment.p_id == p_id,
            func.date(Appointment.start_time) <= datetime.date.today()
        ))
        print(appointments)
        for appointment in appointments:
            item = {
                'Patient ID': p_id, 
                'Name': patient['name'], 
                'Doctor': None, 
                'Date': appointment.start_time.strftime("%d-%m-%Y"), 
                'Start': appointment.start_time.hour, 
                'End':appointment.end_time.hour, 
                'Diagnosis':appointment.diagnosis, 
                'Prescriptions':None
            }
            doctor = db.session.get(Doctor, appointment.d_id)
            item['Doctor'] = doctor.name
            prescriptions = list(Prescription.query.filter(
                Prescription.a_id == appointment.a_id
            ))
            item['Prescriptions'] = ", ".join([p.medicine for p in prescriptions])
            response.append(item)
        return response
