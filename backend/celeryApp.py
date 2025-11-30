from celery import Celery
from celery.schedules import crontab
from app import app
from models import db, Patient, Doctor
from api import Backend_Apis
from mail import send_email
from datetime import datetime, timedelta, date
from flask import render_template
import calendar
import csv
import time
import uuid


celeryApp = Celery(
    'backend_tasks',
    broker='redis://localhost:6379/0'
)

celeryApp.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False,
)

celeryApp.conf.beat_schedule = {
    "daily_reminders": {
        'task': 'celeryApp.send_daily_reminder', 
        'schedule': crontab(hour=8)
    },
    "monthly_report": {
        'task': 'celeryApp.monthly_task',
        'schedule' : crontab(hour=16, minute=22)
    }
}

@celeryApp.task
def send_daily_reminder():
    with app.app_context():
        data = Backend_Apis().daily_reminders(date=datetime.now().date())
        for user in data:
            subject = "Hey there?"
            mail_template = render_template('dailyReminder.html', data=user)
            send_email(user['email'], subject, mail_template)
    return "Sent Daily Reminders!"

@celeryApp.task 
def monthly_task(): 
    today = date.today() 
    ld = calendar.monthrange(today.year, today.month)[1] 
    start = date(day=1, month=today.month, year=today.year) 
    end = date(day=ld, month=today.month, year=today.year) 
    if today.day == ld: 
        with app.app_context(): 
            doctors = list(Doctor.query.all()) 
            response = [] 
            for doctor in doctors: 
                subject = 'Monthly Report' 
                data = Backend_Apis().monthly_report(start=start, end = end, d_id= doctor.d_id) 
                mail_template = render_template('monthlyReport.html', data = data) 
                send_email(doctor.email, subject, mail_template) 
        return "Sent monthly report"
    
@celeryApp.task()
def export_csv(p_id):

    with app.app_context():
        data = Backend_Apis().csv_data(p_id=p_id)
        patient = db.session.get(Patient, p_id)
        print(data)
        with open('static/report.csv', mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        download_link = "http://127.0.0.1:5000/static/report.csv"
        send_email(str(patient.email), 'Report Ready!', f'<h1>Your report is ready!</h1><a href="{download_link}">Download Report</a>')

    return "Report generated"
