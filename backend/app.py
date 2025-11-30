from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
from routes import auth_bp, admin_bp, patient_bp, doctor_bp, report_bp
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from models import db, Admin, Patient, Doctor, Department
from flask_cors import CORS
from cache import cache
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Lhospital.sqlite3"
app.config['JWT_SECRET_KEY'] = "BuffaloWings"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=100)
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

cache.init_app(app)
jwt = JWTManager(app)
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.before_request
def skip_jwt_for_options():
    if request.method == "OPTIONS":
        return '', 200

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(doctor_bp, url_prefix='/doctor')
app.register_blueprint(report_bp, url_prefix='/report')



def create_admin():
    admin = (db.session.query(Admin).all())
    if not admin:

        admin = Admin(
            email="admin@lhospital",
            password=generate_password_hash("admin123"),
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

def create_dept():
    dept = (db.session.query(Department).all())
    if not dept:
        dept1 = Department(
            name="Cardiology",
            description="Get your hearts fixed here",
        )
        
        dept2 = Department(
            name="Pediatrics",
            description="Get your kids fixed here",
        )
        
        dept3 = Department(
            name="Opthalamology",
            description="Get your eyes fixed here",
        )

        db.session.add(dept1)
        db.session.add(dept2)
        db.session.add(dept3)
        db.session.commit()
        print("Departments created successfully.")
    else:
        print("Departments already exists.")

with app.app_context():
    db.create_all()
    create_admin()
    create_dept()

if __name__ == "__main__":
    app.run(port=5000, debug=True)