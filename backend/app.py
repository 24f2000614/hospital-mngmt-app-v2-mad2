from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Admin, Patient, Doctor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Lhospital.sqlite3"
db.init_app(app)

def create_admin():
    admin = (db.session.query(Admin).all())
    if not admin:
        admin = Admin(
            email="admin@L'Hospital",
            password=generate_password_hash("admin123"),
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

with app.app_context():
    db.create_all()
    create_admin()

if __name__ == "__main__":
    app.run(port=5000, debug=True)