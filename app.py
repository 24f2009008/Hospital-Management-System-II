from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect,  flash, jsonify
from flask_restful import Api
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
    UserMixin,
)
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Time,
    Boolean,
    DateTime,
    Text,
    func
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, aliased
from datetime import date, timedelta
from flask_cors import CORS


# --- SQLAlchemy setup ---
engine = create_engine("sqlite:///hms.db", echo=True, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, future=True)


# --- Models ---
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, index=True)  # admin | doctor | patient
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    admin = relationship("Admin", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="admin")
    manages_doctors = relationship("Doctor", back_populates="admin")
    manages_patients = relationship("Patient", back_populates="admin")
    oversees_appointments = relationship("Appointment", back_populates="admin")


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    doctors = relationship("Doctor", back_populates="department")


class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"), unique=True)
    depid = Column(Integer, ForeignKey("department.id"))
    license_number = Column(String(50), unique=True, index=True)
    specialization = Column(String(100))
    qualification = Column(Text)
    experience = Column(Integer)
    gender = Column(String(10))
    status = Column(String(20), default="active")
    admin_id = Column(Integer, ForeignKey("admin.id"))

    user = relationship("User", back_populates="doctor")
    department = relationship("Department", back_populates="doctors")
    admin = relationship("Admin", back_populates="manages_doctors")
    appointments = relationship("Appointment", back_populates="doctor")
    availability = relationship("DoctorAvailability", back_populates="doctor")
    treatments = relationship("Treatment", back_populates="doctor")


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"), unique=True)
    gender = Column(String(10))
    dob = Column(Date)
    blood_group = Column(String(5))
    address = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    admin_id = Column(Integer, ForeignKey("admin.id"))

    user = relationship("User", back_populates="patient")
    admin = relationship("Admin", back_populates="manages_patients")
    appointments = relationship("Appointment", back_populates="patient")
    treatments = relationship("Treatment", back_populates="patient")
    medical_history = relationship(
        "MedicalHistory", back_populates="patient", uselist=False
    )


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True)
    appointment_number = Column(String(20), unique=True, index=True)
    patid = Column(Integer, ForeignKey("patient.id"))
    docid = Column(Integer, ForeignKey("doctor.id"))
    appoint_date = Column(Date)
    appoint_time = Column(Time)
    status = Column(String(20), default="Booked")  # Booked | Completed | Cancelled
    reason_for_visit = Column(Text)
    admin_id = Column(Integer, ForeignKey("admin.id"))

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    admin = relationship("Admin", back_populates="oversees_appointments")
    treatment = relationship("Treatment", back_populates="appointment", uselist=False)


class Treatment(Base):
    __tablename__ = "treatment"

    id = Column(Integer, primary_key=True)
    appointid = Column(Integer, ForeignKey("appointment.id"))
    docid = Column(Integer, ForeignKey("doctor.id"))
    patid = Column(Integer, ForeignKey("patient.id"))
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    prescription = Column(Text)
    notes = Column(Text)
    next_visit_date = Column(Date)
    treatment_date = Column(DateTime, default=datetime.utcnow)

    appointment = relationship("Appointment", back_populates="treatment")
    doctor = relationship("Doctor", back_populates="treatments")
    patient = relationship("Patient", back_populates="treatments")


class DoctorAvailability(Base):
    __tablename__ = "doctor_availability"

    id = Column(Integer, primary_key=True)
    docid = Column(Integer, ForeignKey("doctor.id"))
    available_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    available = Column(Boolean, default=True)
    notes = Column(Text)

    doctor = relationship("Doctor", back_populates="availability")


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id = Column(Integer, primary_key=True)
    patid = Column(Integer, ForeignKey("patient.id"), unique=True)
    allergies = Column(Text)
    chronic_conditions = Column(Text)
    current_medications = Column(Text)
    previous_surgeries = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="medical_history")


# --- Helper functions ---
def calculate_age(dob):
    if not dob:
        return "N/A"
    today = date.today()
    return (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )


def create_super_admin():
    session = SessionLocal()
    admin_username = "admin"
    admin_password = "admin123"
    admin_name = "Hospital Admin"

    try:
        existing_admin = session.query(User).filter_by(username=admin_username).first()
        if existing_admin:
            print("[INFO] Admin user already exists.")
            return

        user = User(
            username=admin_username,
            password=generate_password_hash(admin_password),
            name=admin_name,
            role="admin",
        )
        session.add(user)
        session.commit()

        admin = Admin(uid=user.id)
        session.add(admin)
        session.commit()

        print("[SUCCESS] Super admin created:")
        print(f"Username: {admin_username}")
        print(f"Password: {admin_password}")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] create_super_admin: {e}")
    finally:
        session.close()


def create_standard_departments():
    session = SessionLocal()
    standard_departments = [
        {"name": "Cardiology", "description": "Heart and cardiovascular diseases"},
        {"name": "Neurology", "description": "Brain and nervous system disorders"},
        {"name": "Orthopedics","description": "Bones, joints, and musculoskeletal system",},
        {"name": "Pediatrics","description": "Healthcare for children and adolescents",},
        {"name": "Gynecology", "description": "Female reproductive system health"},
        {"name": "Oncology", "description": "Cancer diagnosis and treatment"},
        {"name": "Dermatology", "description": "Skin, hair, and nail conditions"},
        {"name": "Psychiatry", "description": "Mental health and behavioral disorders"},
        {"name": "Radiology", "description": "Medical imaging and diagnosis"},
        {"name": "Emergency Medicine", "description": "Urgent medical care"},
        {"name": "General Surgery", "description": "Surgical procedures and operations"},
        {"name": "Internal Medicine", "description": "Adult diseases and conditions"},
        {"name": "Ophthalmology", "description": "Eye and vision care"},
        {"name": "ENT", "description": "Ear, Nose, and Throat disorders"},
        {"name": "Urology", "description": "Urinary system and male reproductive organs"},
        {"name": "Dentistry", "description": "Oral health and dental care"},
        {"name": "Physiotherapy", "description": "Physical therapy and rehabilitation"},
        {"name": "Nutrition & Dietetics", "description": "Diet and nutritional guidance"},
    ]

    try:
        for dept_data in standard_departments:
            existing_dept = (
                session.query(Department).filter_by(name=dept_data["name"]).first()
            )
            if not existing_dept:
                department = Department(
                    name=dept_data["name"], description=dept_data["description"]
                )
                session.add(department)
        session.commit()
        print("Standard departments created successfully")
    except Exception as e:
        session.rollback()
        print(f"Error creating departments: {e}")
    finally:
        session.close()

def mark_complete(appointment_id):
    session = SessionLocal()
    try:
        appointment = session.query(Appointment).filter_by(id=appointment_id).first()
        if not appointment:
            flash("Appointment not found.", "warning")
            return redirect("/doctor/appointments")

        appointment.status = "Completed"
        session.commit()
        flash(f"Appointment #{appointment.appointment_number} marked as completed.", "success")
        return redirect("/doctor/appointments")
    except Exception as e:
        print("[ERROR] doctor_mark_complete:", e)
        flash("Error updating appointment.", "danger")
        session.rollback()
        return redirect("/doctor/appointments")
    finally:
        session.close()


def generate_appointment_number(session):
    """
    Generate a sequential appointment number in format APT-XXXX
    """
    try:
        # Get the last appointment number
        last_appointment = session.query(Appointment).order_by(Appointment.id.desc()).first()
        
        if last_appointment and last_appointment.appointment_number:
            # Extract number from format like APT-0012 or APT700498
            apt_num = last_appointment.appointment_number.replace('APT-', '').replace('APT', '')
            try:
                last_num = int(apt_num)
                new_num = last_num + 1
            except ValueError:
                # If parsing fails, start from count
                new_num = session.query(Appointment).count() + 1
        else:
            # No appointments yet, start from 1
            new_num = 1
        
        # Format as APT-XXXX with leading zeros
        appointment_number = f"APT-{new_num:04d}"
        
        # Ensure uniqueness
        while session.query(Appointment).filter_by(appointment_number=appointment_number).first():
            new_num += 1
            appointment_number = f"APT-{new_num:04d}"
        
        return appointment_number
        
    except Exception as e:
        print(f"[ERROR] generate_appointment_number: {e}")
        # Fallback to timestamp-based number
        import time
        return f"APT-{int(time.time()) % 10000:04d}"


def check_doctor_availability(session, doctor_id, appoint_date, appoint_time, exclude_appointment_id=None):
    """
    Check if a doctor is available at the specified date and time.
    Returns (is_available, message)
    """
    try:
        # Check if doctor exists and is active
        doctor = session.query(Doctor).filter_by(id=doctor_id, status="active").first()
        if not doctor:
            return False, "Selected doctor is not available."
        
        # Check for conflicting appointments
        query = session.query(Appointment).filter_by(
            docid=doctor_id,
            appoint_date=appoint_date,
            appoint_time=appoint_time
        ).filter(Appointment.status != "Cancelled")
        
        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)
        
        existing = query.first()
        if existing:
            return False, "This time slot is already booked. Please choose another time."
        
        # Check doctor availability table (if exists)
        availability = session.query(DoctorAvailability).filter_by(
            docid=doctor_id,
            available_date=appoint_date
        ).first()
        
        if availability and not availability.available:
            return False, "Doctor is not available on this date. Please choose another date."
        
        # If availability record exists, check time range
        if availability:
            if availability.start_time and availability.end_time:
                if not (availability.start_time <= appoint_time <= availability.end_time):
                    return False, f"Doctor is only available between {availability.start_time.strftime('%H:%M')} and {availability.end_time.strftime('%H:%M')}."
        
        return True, "Time slot is available."
        
    except Exception as e:
        print(f"[ERROR] check_doctor_availability: {e}")
        return False, "Error checking availability. Please try again."

# --- Flask app setup ---
app = Flask(__name__)
# CORS(app,resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Enable CORS for all origins on specific routes
CORS(
    app,
    supports_credentials=True,                    # ← Required for cookies / Flask-Login session
    origins=["http://localhost:5173", "http://127.0.0.1:5173"],   # Exact origins          # ← Your Vite dev server origin
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
app.secret_key = "secret_key"

# Initialize Flask-RESTful API
api = Api(app)

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_api"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    try:
        user = session.get(User, int(user_id))
        if user and user.is_active:
            return user
        return None
    except Exception as e:
        print(f"Error loading user {user_id}: {e}")
        return None
    finally:
        session.close()



@app.context_processor
def inject_user():
    try:
        if current_user.is_authenticated and hasattr(current_user, "name"):
            return dict(current_user=current_user, now=datetime.now())
    except Exception as e:
        print(f"Context processor error: {e}")

    class SafeUser:
        is_authenticated = False
        name = "Guest"
        role = "guest"

    return dict(current_user=SafeUser(), now=datetime.now())



@app.route("/")
def main():
    return render_template("dashboard.html")


@app.route("/api/login", methods=["POST"])
def login_api():
    logout_user()

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    session = SessionLocal()

    try:
        user = session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return jsonify({
                "success": True,
                "message": "Login successful",
                "role": user.role,
                "user_id": user.id
            })

        else:
            return jsonify({
                "success": False,
                "message": "Invalid username or password"
            }), 401

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        session.close()

@app.route("/api/register", methods=["POST"])
def api_register():

    data = request.get_json()
    session = SessionLocal()

    try:
        name = data.get("name", "").strip()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        gender = data.get("gender")
        dob = data.get("dob")
        blood_group = data.get("bloodGrp")
        address = data.get("address")

        if not all([name, username, password, gender, dob, blood_group, address]):
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Username already exists"
            }), 400

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password,
            name=name,
            role="patient"
        )

        session.add(user)
        session.flush()  

        new_patient = Patient(
            uid=user.id,
            gender=gender,
            dob=datetime.strptime(dob, "%Y-%m-%d").date(),
            blood_group=blood_group,
            address=address,
            is_active=True
        )

        session.add(new_patient)
        session.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful",
            "role": user.role,
            "user_id": user.id
        }), 201

    except Exception as e:
        session.rollback()
        print(f"Register error: {e}")

        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        session.close()

@app.route("/api/logout", methods=["POST"])
@login_required
def logout_api():
    logout_user()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200

@app.route("/api/dashboard", methods=["GET"])
@login_required
def dashboard_api():
    return jsonify({
        "success": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role
        }
    }), 200

            
@app.route("/api/admin/dashboard", methods=["GET"])
def admin_dashboard_api():
    if not current_user.is_authenticated or getattr(current_user, 'role', None) != "admin":
        return jsonify({
            "success": False,
            "message": "Authentication required. Please log in as admin."
        }), 401

    session = SessionLocal()
    try:
        total_doctors = session.query(Doctor).count()
        total_patients = session.query(Patient).count()
        total_appointments = session.query(Appointment).count()

        doctors = session.query(Doctor).join(User).join(Department)\
            .order_by(Doctor.id.desc()).limit(5).all()

        patients = session.query(Patient).join(User)\
            .order_by(Patient.id.desc()).limit(5).all()

        appointments = session.query(Appointment).join(Doctor).join(Patient)\
            .order_by(Appointment.appoint_date.desc(), Appointment.appoint_time.desc())\
            .limit(10).all()

        departments = session.query(Department).order_by(Department.name).all()

        return jsonify({
            "success": True,
            "stats": {
                "doctors": total_doctors,
                "patients": total_patients,
                "appointments": total_appointments
            },
            "recent_doctors": [
                {
                    "id": d.id,
                    "name": d.user.name,
                    "specialization": d.department.name
                } for d in doctors
            ],
            "recent_patients": [
                {
                    "id": p.id,
                    "name": p.user.name
                } for p in patients
            ],
            "recent_appointments": [
                {
                    "id": a.id,
                    "doctor": a.doctor.user.name,
                    "patient": a.patient.user.name,
                    "date": str(a.appoint_date),
                    "time": str(a.appoint_time),
                    "status": a.status
                } for a in appointments
            ],
            "departments": [
                {
                    "id": d.id,
                    "name": d.name
                } for d in departments
            ]
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin dashboard: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading dashboard"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/dashboard", methods=["GET"])
@login_required
def patient_dashboard():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient not found"
            }), 404

        upcoming_appointments = session.query(Appointment).filter_by(
            patid=patient.id,
            status="Booked"
        ).filter(Appointment.appoint_date >= date.today()).count()

        total_appointments = session.query(Appointment).filter_by(
            patid=patient.id
        ).count()

        doctors = session.query(Doctor, User, Department).join(
            User, Doctor.uid == User.id
        ).outerjoin(
            Department, Doctor.depid == Department.id
        ).filter(Doctor.status == "active").limit(6).all()

        doctors_list = [
            {
                "id": doctor.id,
                "name": user.name,
                "department": dept.name if dept else "General",
                "qualification": doctor.qualification or "N/A",
                "experience": doctor.experience,
                "specialization": doctor.specialization
            }
            for doctor, user, dept in doctors
        ]

        recent_appointments = session.query(Appointment).filter_by(
            patid=patient.id
        ).order_by(
            Appointment.appoint_date.desc(),
            Appointment.appoint_time.desc()
        ).limit(5).all()

        appointments_list = [
            {
                "id": apt.id,
                "doctor_name": apt.doctor.user.name if apt.doctor and apt.doctor.user else "N/A",
                "date": apt.appoint_date.strftime('%Y-%m-%d') if apt.appoint_date else "N/A",
                "time": apt.appoint_time.strftime('%H:%M') if apt.appoint_time else "N/A",
                "reason": apt.reason_for_visit or "N/A",
                "status": apt.status
            }
            for apt in recent_appointments
        ]

        return jsonify({
            "success": True,
            "stats": {
                "total_appointments": total_appointments,
                "upcoming": upcoming_appointments
            },
            "doctors": doctors_list,
            "appointments": appointments_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Patient dashboard: {e}")

        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        session.close()

@app.route("/api/doctor/dashboard", methods=["GET"])
@login_required
def doctor_dashboard_api():

    # ✅ Role check
    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        # ✅ Get doctor once
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        today = date.today()
        next_week = today + timedelta(days=7)

        # ✅ Stats
        todays_appointments = session.query(Appointment).filter(
            Appointment.docid == doctor.id,
            Appointment.appoint_date == today
        ).count()

        pending_consultations = session.query(Appointment).filter(
            Appointment.docid == doctor.id,
            Appointment.status == "Booked"
        ).count()

        upcoming_appointments = session.query(Appointment).filter(
            Appointment.docid == doctor.id,
            Appointment.appoint_date.between(today, next_week)
        ).count()

        # ✅ Assigned patients (with user join)
        assigned_patients = (
            session.query(Patient)
            .join(User, User.id == Patient.uid)
            .join(Appointment, Appointment.patid == Patient.id)
            .filter(Appointment.docid == doctor.id)
            .group_by(Patient.id, User.name)
            .order_by(func.max(Appointment.appoint_date).desc())
            .limit(5)
            .all()
        )

        # ✅ Serialize patients
        patients_data = [
            {
                "id": p.id,
                "name": p.user.name
            }
            for p in assigned_patients
        ]

        # ✅ Chart data
        chart_start = today - timedelta(days=6)

        daily_counts = (
            session.query(Appointment.appoint_date, func.count(Appointment.id))
            .filter(
                Appointment.docid == doctor.id,
                Appointment.appoint_date >= chart_start
            )
            .group_by(Appointment.appoint_date)
            .order_by(Appointment.appoint_date)
            .all()
        )

        chart_data = {
            "dates": [str(d[0]) for d in daily_counts],
            "counts": [d[1] for d in daily_counts],
        }

        return jsonify({
            "success": True,
            "stats": {
                "todays_appointments": todays_appointments,
                "pending_consultations": pending_consultations,
                "upcoming_appointments": upcoming_appointments
            },
            "assigned_patients": patients_data,
            "chart_data": chart_data,
            "appointments": []
        }), 200

    except Exception as e:
        print(f"[ERROR] Doctor dashboard: {e}")

        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/doctors", methods=["GET"])
@login_required
def patient_doctor_search():
    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()
    try:
        search_query = request.args.get("search", "").strip()
        specialization = request.args.get("specialization", "").strip()
        department_filter = request.args.get("department", "").strip()

        query = session.query(Doctor, User, Department).join(
            User, Doctor.uid == User.id
        ).outerjoin(
            Department, Doctor.depid == Department.id
        ).filter(Doctor.status == "active")

        # Search by name
        if search_query:
            query = query.filter(User.name.ilike(f"%{search_query}%"))

        # Filter by specialization
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))

        # Filter by department (case-insensitive)
        if department_filter:
            query = query.filter(Department.name.ilike(f"%{department_filter}%"))

        results = query.all()

        doctors = [
            {
                "id": doctor.id,
                "name": user.name,
                "department": dept.name if dept else "General",
                "specialization": doctor.specialization or "General Physician",
                "qualification": doctor.qualification or "N/A",
                "experience": doctor.experience or 0,
                "username": user.username
            }
            for doctor, user, dept in results
        ]
        departments = session.query(Department).all()
        departments_list = [
            {
                "id": d.id,
                "name": d.name
            }
            for d in departments
        ]

        return jsonify({
            "success": True,
            "doctors": doctors,
            "departments": departments_list,
            "filters": {
                "search": search_query,
                "specialization": specialization,
                "department": department_filter
            }
        }), 200

    except Exception as e:
        print(f"[ERROR] patient_doctor_search:", e)

        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/appointments", methods=["GET"])
@login_required
def patient_appointments():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient not found"
            }), 404

        appointments = session.query(Appointment).filter_by(
            patid=patient.id
        ).order_by(
            Appointment.appoint_date.desc(),
            Appointment.appoint_time.desc()
        ).all()

        appointments_list = [
            {
                "id": apt.id,
                "doctor_name": apt.doctor.user.name if apt.doctor and apt.doctor.user else "N/A",
                "date": apt.appoint_date.strftime("%Y-%m-%d") if apt.appoint_date else None,
                "time": apt.appoint_time.strftime("%H:%M") if apt.appoint_time else None,
                "status": apt.status,
                "reason": apt.reason_for_visit or "",
                "diagnosis": apt.treatment.diagnosis if hasattr(apt, "treatment") and apt.treatment else None,
                "prescription": apt.treatment.prescription if hasattr(apt, "treatment") and apt.treatment else None
            }
            for apt in appointments
        ]

        return jsonify({
            "success": True,
            "appointments": appointments_list
        }), 200

    except Exception as e:
        print("[ERROR] patient_appointments:", e)

        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/appointments/book", methods=["POST"])
@login_required
def patient_book_appointment():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        doctor_id = data.get("doctor_id")
        appoint_date_str = data.get("appoint_date")
        appoint_time_str = data.get("appoint_time")
        reason = data.get("reason")

        if not all([doctor_id, appoint_date_str, appoint_time_str, reason]):
            return jsonify({
                "success": False,
                "message": "All fields are required"
            }), 400

        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        try:
            appoint_date = datetime.strptime(appoint_date_str, "%Y-%m-%d").date()
            appoint_time = datetime.strptime(appoint_time_str, "%H:%M").time()
        except:
            return jsonify({
                "success": False,
                "message": "Invalid date or time format"
            }), 400

        if appoint_date < date.today():
            return jsonify({
                "success": False,
                "message": "Cannot book appointments in the past"
            }), 400

        existing = session.query(Appointment).filter_by(
            docid=doctor_id,
            appoint_date=appoint_date,
            appoint_time=appoint_time,
            status="Booked"
        ).first()

        if existing:
            return jsonify({
                "success": False,
                "message": "Time slot already booked"
            }), 409

        appointment_number = generate_appointment_number(session)

        appointment = Appointment(
            appointment_number=appointment_number,
            patid=patient.id,
            docid=doctor_id,
            appoint_date=appoint_date,
            appoint_time=appoint_time,
            reason_for_visit=reason,
            status="Booked"
        )

        session.add(appointment)
        session.commit()

        return jsonify({
            "success": True,
            "message": "Appointment booked successfully",
            "appointment_number": appointment_number
        }), 201

    except Exception as e:
        session.rollback()
        print("[ERROR] patient_book_appointment:", e)

        return jsonify({
            "success": False,
            "message": "Error booking appointment"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/appointments/<int:appointment_id>/reschedule", methods=["PUT"])
@login_required
def patient_reschedule_appointment(appointment_id):

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        new_date_str = data.get("appoint_date")
        new_time_str = data.get("appoint_time")

        if not all([new_date_str, new_time_str]):
            return jsonify({
                "success": False,
                "message": "Date and time are required"
            }), 400

        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            patid=patient.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        if appointment.status != "Booked":
            return jsonify({
                "success": False,
                "message": "Only booked appointments can be rescheduled"
            }), 400

        try:
            new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
            new_time = datetime.strptime(new_time_str, "%H:%M").time()
        except:
            return jsonify({
                "success": False,
                "message": "Invalid date or time format"
            }), 400

        if new_date < date.today():
            return jsonify({
                "success": False,
                "message": "Cannot reschedule to a past date"
            }), 400

        existing = session.query(Appointment).filter(
            Appointment.docid == appointment.docid,
            Appointment.appoint_date == new_date,
            Appointment.appoint_time == new_time,
            Appointment.status == "Booked",
            Appointment.id != appointment_id
        ).first()

        if existing:
            return jsonify({
                "success": False,
                "message": "Time slot already booked"
            }), 409

        appointment.appoint_date = new_date
        appointment.appoint_time = new_time

        session.commit()

        return jsonify({
            "success": True,
            "message": "Appointment rescheduled successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] patient_reschedule_appointment:", e)

        return jsonify({
            "success": False,
            "message": "Error rescheduling appointment"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/appointments/<int:appointment_id>/cancel", methods=["PUT"])
@login_required
def patient_cancel_appointment(appointment_id):

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            patid=patient.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        if appointment.status != "Booked":
            return jsonify({
                "success": False,
                "message": "Only booked appointments can be cancelled"
            }), 400

        appointment.status = "Cancelled"
        session.commit()

        return jsonify({
            "success": True,
            "message": "Appointment cancelled successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] patient_cancel_appointment:", e)

        return jsonify({
            "success": False,
            "message": "Error cancelling appointment"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/appointments/<int:appointment_id>", methods=["GET"])
@login_required
def patient_view_appointment(appointment_id):

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            patid=patient.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        return jsonify({
            "success": True,
            "appointment": {
                "id": appointment.id,
                "appointment_number": appointment.appointment_number,
                "doctor_name": appointment.doctor.user.name if appointment.doctor and appointment.doctor.user else "N/A",
                "date": appointment.appoint_date.strftime("%Y-%m-%d") if appointment.appoint_date else None,
                "time": appointment.appoint_time.strftime("%H:%M") if appointment.appoint_time else None,
                "status": appointment.status,
                "reason": appointment.reason_for_visit or "",
                "diagnosis": appointment.treatment.diagnosis if hasattr(appointment, "treatment") and appointment.treatment else None,
                "prescription": appointment.treatment.prescription if hasattr(appointment, "treatment") and appointment.treatment else None,
                "notes": appointment.treatment.notes if hasattr(appointment, "treatment") and appointment.treatment else None
            }
        }), 200

    except Exception as e:
        print("[ERROR] patient_view_appointment:", e)

        return jsonify({
            "success": False,
            "message": "Error loading appointment details"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/appointments/<int:appointment_id>/details", methods=["GET"])
@login_required
def patient_appointment_details(appointment_id):

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            patid=patient.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        return jsonify({
            "success": True,
            "appointment": {
                "id": appointment.id,
                "appointment_number": appointment.appointment_number,
                "doctor_name": appointment.doctor.user.name if appointment.doctor and appointment.doctor.user else "N/A",
                "doctor_specialization": appointment.doctor.specialization if appointment.doctor else "N/A",
                "date": appointment.appoint_date.strftime("%Y-%m-%d") if appointment.appoint_date else None,
                "time": appointment.appoint_time.strftime("%H:%M") if appointment.appoint_time else None,
                "status": appointment.status,
                "reason": appointment.reason_for_visit or "",
                "diagnosis": appointment.treatment.diagnosis if hasattr(appointment, "treatment") and appointment.treatment else None,
                "prescription": appointment.treatment.prescription if hasattr(appointment, "treatment") and appointment.treatment else None,
                "notes": appointment.treatment.notes if hasattr(appointment, "treatment") and appointment.treatment else None
            }
        }), 200

    except Exception as e:
        print("[ERROR] patient_appointment_details:", e)

        return jsonify({
            "success": False,
            "message": "Error loading appointment details"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/treatments", methods=["GET"])
@login_required
def patient_treatment_history():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        treatments = session.query(Treatment).filter_by(
            patid=patient.id
        ).order_by(
            Treatment.treatment_date.desc()
        ).all()

        treatments_list = [
            {
                "id": t.id,
                "appointment_id": t.appointment_id,
                "doctor_name": t.appointment.doctor.user.name if t.appointment and t.appointment.doctor and t.appointment.doctor.user else "N/A",
                "date": t.treatment_date.strftime("%Y-%m-%d") if t.treatment_date else None,
                "diagnosis": t.diagnosis or "",
                "prescription": t.prescription or "",
                "notes": t.notes or ""
            }
            for t in treatments
        ]

        return jsonify({
            "success": True,
            "treatments": treatments_list
        }), 200

    except Exception as e:
        print("[ERROR] patient_treatment_history:", e)

        return jsonify({
            "success": False,
            "message": "Error loading treatment history"
        }), 500

    finally:
        session.close()


@app.route("/api/patient/history", methods=["GET"])
@login_required
def patient_medical_history():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        medical_history = session.query(MedicalHistory).filter_by(
            patid=patient.id
        ).first()

        treatments = session.query(Treatment).filter_by(
            patid=patient.id
        ).order_by(
            Treatment.treatment_date.desc()
        ).all()

        appointments = session.query(Appointment).filter_by(
            patid=patient.id
        ).order_by(
            Appointment.appoint_date.desc()
        ).all()

        treatments_list = [
            {
                "id": t.id,
                "appointment_id": t.appointment_id,
                "doctor_name": t.appointment.doctor.user.name if t.appointment and t.appointment.doctor and t.appointment.doctor.user else "N/A",
                "date": t.treatment_date.strftime("%Y-%m-%d") if t.treatment_date else None,
                "diagnosis": t.diagnosis or "",
                "prescription": t.prescription or "",
                "notes": t.notes or ""
            }
            for t in treatments
        ]

        appointments_list = [
            {
                "id": a.id,
                "doctor_name": a.doctor.user.name if a.doctor and a.doctor.user else "N/A",
                "date": a.appoint_date.strftime("%Y-%m-%d") if a.appoint_date else None,
                "time": a.appoint_time.strftime("%H:%M") if a.appoint_time else None,
                "status": a.status,
                "reason": a.reason_for_visit or ""
            }
            for a in appointments
        ]

        return jsonify({
            "success": True,
            "patient": {
                "id": patient.id,
                "name": patient.user.name if hasattr(patient, "user") and patient.user else ""
            },
            "medical_history": {
                "allergies": medical_history.allergies if medical_history else "",
                "chronic_conditions": medical_history.chronic_conditions if medical_history else "",
                "medications": medical_history.medications if medical_history else "",
                "notes": medical_history.notes if medical_history else ""
            },
            "treatments": treatments_list,
            "appointments": appointments_list
        }), 200

    except Exception as e:
        print("[ERROR] patient_medical_history:", e)

        return jsonify({
            "success": False,
            "message": "Error loading medical history"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/doctors", methods=["POST"])
@login_required
def add_doctor():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        gender = data.get("gender")
        department_id = data.get("department")
        license_number = data.get("license_number")
        specialization = data.get("specialization")
        qualification = data.get("qualification")
        experience = data.get("experience", 0)

        if not all([name, username, password, gender, department_id, license_number, specialization, qualification]):
            return jsonify({
                "success": False,
                "message": "All required fields must be provided"
            }), 400

        try:
            experience = int(experience)
            if experience < 0:
                return jsonify({
                    "success": False,
                    "message": "Experience cannot be negative"
                }), 400
        except:
            return jsonify({
                "success": False,
                "message": "Invalid experience value"
            }), 400

        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Username already exists"
            }), 400

        existing_license = session.query(Doctor).filter_by(license_number=license_number).first()
        if existing_license:
            return jsonify({
                "success": False,
                "message": "License number already registered"
            }), 400

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password,
            name=name,
            role="doctor"
        )

        session.add(user)
        session.flush()

        admin_record = session.query(Admin).filter_by(uid=current_user.id).first()

        new_doctor = Doctor(
            uid=user.id,
            depid=int(department_id),
            license_number=license_number,
            specialization=specialization,
            qualification=qualification,
            experience=experience,
            gender=gender,
            admin_id=admin_record.id if admin_record else None
        )

        session.add(new_doctor)
        session.commit()

        return jsonify({
            "success": True,
            "message": "Doctor added successfully",
            "doctor": {
                "id": new_doctor.id,
                "name": name,
                "username": username,
                "specialization": specialization
            }
        }), 201

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Add Doctor failed: {e}")

        return jsonify({
            "success": False,
            "message": "Error adding doctor"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/doctors", methods=["GET"])
@login_required
def admin_doctors():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctors = session.query(Doctor, User, Department).join(
            User, Doctor.uid == User.id
        ).join(
            Department, Doctor.depid == Department.id
        ).order_by(Doctor.id.desc()).all()

        doctors_list = [
            {
                "id": doctor.id,
                "name": user.name,
                "username": user.username,
                "department": department.name,
                "specialization": doctor.specialization,
                "qualification": doctor.qualification,
                "experience": doctor.experience,
                "license_number": doctor.license_number,
                "gender": doctor.gender
            }
            for doctor, user, department in doctors
        ]

        departments = session.query(Department).order_by(Department.name).all()
        departments_list = [
            {
                "id": d.id,
                "name": d.name
            }
            for d in departments
        ]

        return jsonify({
            "success": True,
            "doctors": doctors_list,
            "departments": departments_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin doctors: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading doctors"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/doctors/<int:doctor_id>", methods=["PUT"])
@login_required
def update_doctor(doctor_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        doctor = session.query(Doctor).filter_by(id=doctor_id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor not found"
            }), 404

        specialization = data.get("specialization")
        qualification = data.get("qualification")
        experience = data.get("experience")
        department = data.get("department")
        name = data.get("name")

        if specialization:
            doctor.specialization = specialization

        if qualification:
            doctor.qualification = qualification

        if experience is not None:
            try:
                exp_val = int(experience)
                if exp_val < 0:
                    return jsonify({
                        "success": False,
                        "message": "Experience cannot be negative"
                    }), 400
                doctor.experience = exp_val
            except:
                return jsonify({
                    "success": False,
                    "message": "Invalid experience value"
                }), 400

        if department:
            doctor.depid = int(department)

        if name and doctor.user:
            doctor.user.name = name

        session.commit()

        return jsonify({
            "success": True,
            "message": "Doctor updated successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Update doctor: {e}")

        return jsonify({
            "success": False,
            "message": "Error updating doctor"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/doctors/<int:doctor_id>/status", methods=["PUT"])
@login_required
def toggle_doctor_status(doctor_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()
        update_status = data.get("status", "").lower().strip()

        if update_status not in ["active", "inactive"]:
            return jsonify({
                "success": False,
                "message": "Invalid status value"
            }), 400

        doctor = session.query(Doctor).filter_by(id=doctor_id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor not found"
            }), 404

        if update_status == "inactive":
            if doctor.status == "inactive":
                return jsonify({
                    "success": False,
                    "message": "Doctor is already inactive"
                }), 400

            doctor.status = "inactive"
            if doctor.user:
                doctor.user.is_active = False

        elif update_status == "active":
            if doctor.status == "active":
                return jsonify({
                    "success": False,
                    "message": "Doctor is already active"
                }), 400

            doctor.status = "active"
            if doctor.user:
                doctor.user.is_active = True

        session.commit()

        return jsonify({
            "success": True,
            "message": f"Doctor status updated to {update_status}"
        }), 200

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Toggle doctor status: {e}")

        return jsonify({
            "success": False,
            "message": "Error updating doctor status"
        }), 500

    finally:
        session.close()



@app.route("/api/admin/patients", methods=["GET"])
@login_required
def admin_patients():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patients = session.query(Patient, User).join(
            User, Patient.uid == User.id
        ).order_by(Patient.id.desc()).all()

        patients_list = [
            {
                "id": patient.id,
                "name": user.name,
                "username": user.username,
                "gender": patient.gender,
                "dob": patient.dob.strftime("%Y-%m-%d") if patient.dob else None,
                "blood_group": patient.blood_group,
                "address": patient.address,
                "is_active": patient.is_active
            }
            for patient, user in patients
        ]

        return jsonify({
            "success": True,
            "patients": patients_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin patients: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading patients"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/patients/<int:patient_id>/toggle", methods=["PUT"])
@login_required
def toggle_patient_status(patient_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(id=patient_id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient not found"
            }), 404

        patient.is_active = not patient.is_active

        if patient.user:
            patient.user.is_active = patient.is_active

        session.commit()

        return jsonify({
            "success": True,
            "message": f"Patient {'activated' if patient.is_active else 'deactivated'} successfully",
            "is_active": patient.is_active
        }), 200

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Toggle patient status: {e}")

        return jsonify({
            "success": False,
            "message": "Error updating patient status"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/appointments", methods=["GET"])
@login_required
def admin_appointments():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        filter_status = request.args.get("status", "all")
        filter_date = request.args.get("date", "all")

        query = session.query(Appointment).join(
            Doctor, Appointment.docid == Doctor.id
        ).join(
            Patient, Appointment.patid == Patient.id
        )

        if filter_status != "all":
            query = query.filter(Appointment.status == filter_status)

        today = date.today()
        if filter_date == "upcoming":
            query = query.filter(Appointment.appoint_date >= today)
        elif filter_date == "past":
            query = query.filter(Appointment.appoint_date < today)

        appointments = query.order_by(
            Appointment.appoint_date.desc(),
            Appointment.appoint_time.desc()
        ).all()

        appointments_list = [
            {
                "id": apt.id,
                "appointment_number": apt.appointment_number,
                "doctor_name": apt.doctor.user.name if apt.doctor and apt.doctor.user else "N/A",
                "patient_name": apt.patient.user.name if apt.patient and apt.patient.user else "N/A",
                "date": apt.appoint_date.strftime("%Y-%m-%d") if apt.appoint_date else None,
                "time": apt.appoint_time.strftime("%H:%M") if apt.appoint_time else None,
                "status": apt.status,
                "reason": apt.reason_for_visit or ""
            }
            for apt in appointments
        ]

        return jsonify({
            "success": True,
            "appointments": appointments_list,
            "filters": {
                "status": filter_status,
                "date": filter_date
            }
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin appointments: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading appointments"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/search", methods=["GET"])
@login_required
def admin_search():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        query_param = request.args.get("query", "").strip()

        doctors = session.query(Doctor, User, Department).join(
            User, Doctor.uid == User.id
        ).outerjoin(
            Department, Doctor.depid == Department.id
        )

        patients = session.query(Patient, User).join(
            User, Patient.uid == User.id
        )

        if query_param:
            doctors = doctors.filter(
                (User.name.ilike(f"%{query_param}%")) |
                (Doctor.specialization.ilike(f"%{query_param}%"))
            )

            patients = patients.filter(
                (User.name.ilike(f"%{query_param}%")) |
                (User.username.ilike(f"%{query_param}%"))
            )

        doctors_list = [
            {
                "id": d.id,
                "name": u.name,
                "username": u.username,
                "department": dept.name if dept else "General",
                "specialization": d.specialization,
                "status": d.status
            }
            for d, u, dept in doctors.all()
        ]

        patients_list = [
            {
                "id": p.id,
                "name": u.name,
                "username": u.username,
                "gender": p.gender,
                "is_active": p.is_active
            }
            for p, u in patients.all()
        ]

        return jsonify({
            "success": True,
            "query": query_param,
            "doctors": doctors_list,
            "patients": patients_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin search: {e}")

        return jsonify({
            "success": False,
            "message": "Error performing search"
        }), 500

    finally:
        session.close()

@app.route("/api/admin/departments", methods=["GET"])
@login_required
def admin_departments():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        departments = session.query(Department).order_by(Department.name).all()

        dept_list = [
            {
                "id": dept.id,
                "name": dept.name,
                "description": dept.description,
                "doctor_count": session.query(Doctor).filter_by(depid=dept.id).count(),
                "created_at": dept.created_at.strftime("%Y-%m-%d") if dept.created_at else None
            }
            for dept in departments
        ]

        return jsonify({
            "success": True,
            "departments": dept_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin departments: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading departments"
        }), 500

    finally:
        session.close()

@app.route("/api/admin/departments", methods=["POST"])
@login_required
def add_department():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        name = data.get("name", "").strip()
        description = data.get("description", "").strip()

        if not name:
            return jsonify({
                "success": False,
                "message": "Department name is required"
            }), 400

        existing = session.query(Department).filter_by(name=name).first()
        if existing:
            return jsonify({
                "success": False,
                "message": "Department already exists"
            }), 400

        new_dept = Department(name=name, description=description)
        session.add(new_dept)
        session.commit()

        return jsonify({
            "success": True,
            "message": "Department added successfully",
            "department": {
                "id": new_dept.id,
                "name": new_dept.name
            }
        }), 201

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Add department: {e}")

        return jsonify({
            "success": False,
            "message": "Error adding department"
        }), 500

    finally:
        session.close()

@app.route("/api/admin/departments/<int:dept_id>", methods=["PUT"])
@login_required
def update_department(dept_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        dept = session.query(Department).filter_by(id=dept_id).first()

        if not dept:
            return jsonify({
                "success": False,
                "message": "Department not found"
            }), 404

        name = data.get("name")
        description = data.get("description")

        if name:
            dept.name = name.strip()

        if description:
            dept.description = description.strip()

        session.commit()

        return jsonify({
            "success": True,
            "message": "Department updated successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print(f"[ERROR] Update department: {e}")

        return jsonify({
            "success": False,
            "message": "Error updating department"
        }), 500

    finally:
        session.close()
        

@app.route("/api/admin/reports", methods=["GET"])
@login_required
def admin_reports():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        total_doctors = session.query(Doctor).count()
        active_doctors = session.query(Doctor).filter_by(status="active").count()
        inactive_doctors = total_doctors - active_doctors

        total_patients = session.query(Patient).count()
        active_patients = session.query(Patient).filter_by(is_active=True).count()
        inactive_patients = total_patients - active_patients

        total_appointments = session.query(Appointment).count()
        booked_appointments = session.query(Appointment).filter_by(status="Booked").count()
        completed_appointments = session.query(Appointment).filter_by(status="Completed").count()
        cancelled_appointments = session.query(Appointment).filter_by(status="Cancelled").count()

        departments = session.query(Department).all()
        dept_stats = [
            {
                "name": dept.name,
                "doctor_count": session.query(Doctor).filter_by(depid=dept.id).count()
            }
            for dept in departments
        ]

        recent_doctors = session.query(Doctor).join(User).order_by(User.created_at.desc()).limit(5).all()
        recent_patients = session.query(Patient).join(User).order_by(User.created_at.desc()).limit(5).all()
        recent_appointments = session.query(Appointment).order_by(Appointment.id.desc()).limit(5).all()

        recent_doctors_list = [
            {
                "id": d.id,
                "name": d.user.name if d.user else "",
                "created_at": d.user.created_at.strftime("%Y-%m-%d") if d.user and d.user.created_at else None
            }
            for d in recent_doctors
        ]

        recent_patients_list = [
            {
                "id": p.id,
                "name": p.user.name if p.user else "",
                "created_at": p.user.created_at.strftime("%Y-%m-%d") if p.user and p.user.created_at else None
            }
            for p in recent_patients
        ]

        recent_appointments_list = [
            {
                "id": a.id,
                "appointment_number": a.appointment_number,
                "doctor_name": a.doctor.user.name if a.doctor and a.doctor.user else "N/A",
                "patient_name": a.patient.user.name if a.patient and a.patient.user else "N/A",
                "date": a.appoint_date.strftime("%Y-%m-%d") if a.appoint_date else None,
                "status": a.status
            }
            for a in recent_appointments
        ]

        return jsonify({
            "success": True,
            "stats": {
                "doctors": {
                    "total": total_doctors,
                    "active": active_doctors,
                    "inactive": inactive_doctors
                },
                "patients": {
                    "total": total_patients,
                    "active": active_patients,
                    "inactive": inactive_patients
                },
                "appointments": {
                    "total": total_appointments,
                    "booked": booked_appointments,
                    "completed": completed_appointments,
                    "cancelled": cancelled_appointments
                }
            },
            "departments": dept_stats,
            "recent": {
                "doctors": recent_doctors_list,
                "patients": recent_patients_list,
                "appointments": recent_appointments_list
            }
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin reports: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading reports"
        }), 500

    finally:
        session.close()


@app.route("/api/admin/patients/<int:patient_id>/treatments", methods=["GET"])
@login_required
def admin_patient_treatments(patient_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(id=patient_id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient not found"
            }), 404

        treatments = session.query(Treatment).filter_by(
            patid=patient_id
        ).order_by(
            Treatment.treatment_date.desc()
        ).all()

        appointments = session.query(Appointment).filter_by(
            patid=patient_id
        ).order_by(
            Appointment.appoint_date.desc()
        ).all()

        medical_history = session.query(MedicalHistory).filter_by(
            patid=patient_id
        ).first()

        treatments_list = [
            {
                "id": t.id,
                "doctor_name": t.appointment.doctor.user.name if t.appointment and t.appointment.doctor and t.appointment.doctor.user else "N/A",
                "date": t.treatment_date.strftime("%Y-%m-%d") if t.treatment_date else None,
                "diagnosis": t.diagnosis or "",
                "prescription": t.prescription or "",
                "notes": t.notes or ""
            }
            for t in treatments
        ]

        appointments_list = [
            {
                "id": a.id,
                "appointment_number": a.appointment_number,
                "doctor_name": a.doctor.user.name if a.doctor and a.doctor.user else "N/A",
                "date": a.appoint_date.strftime("%Y-%m-%d") if a.appoint_date else None,
                "time": a.appoint_time.strftime("%H:%M") if a.appoint_time else None,
                "status": a.status
            }
            for a in appointments
        ]

        return jsonify({
            "success": True,
            "patient": {
                "id": patient.id,
                "name": patient.user.name if hasattr(patient, "user") and patient.user else ""
            },
            "medical_history": {
                "allergies": medical_history.allergies if medical_history else "",
                "chronic_conditions": medical_history.chronic_conditions if medical_history else "",
                "medications": medical_history.medications if medical_history else "",
                "notes": medical_history.notes if medical_history else ""
            },
            "treatments": treatments_list,
            "appointments": appointments_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin patient treatments: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading patient treatments"
        }), 500

    finally:
        session.close()

@app.route("/api/admin/treatments", methods=["GET"])
@login_required
def admin_treatments():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        filter_doctor = request.args.get("doctor_id", "")
        filter_patient = request.args.get("patient_id", "")

        query = session.query(Treatment).join(
            Doctor, Treatment.docid == Doctor.id
        ).join(
            Patient, Treatment.patid == Patient.id
        )

        if filter_doctor:
            query = query.filter(Treatment.docid == int(filter_doctor))

        if filter_patient:
            query = query.filter(Treatment.patid == int(filter_patient))

        treatments = query.order_by(
            Treatment.treatment_date.desc()
        ).all()

        treatments_list = [
            {
                "id": t.id,
                "doctor_id": t.docid,
                "patient_id": t.patid,
                "doctor_name": t.appointment.doctor.user.name if t.appointment and t.appointment.doctor and t.appointment.doctor.user else "N/A",
                "patient_name": t.appointment.patient.user.name if t.appointment and t.appointment.patient and t.appointment.patient.user else "N/A",
                "date": t.treatment_date.strftime("%Y-%m-%d") if t.treatment_date else None,
                "diagnosis": t.diagnosis or "",
                "prescription": t.prescription or "",
                "notes": t.notes or ""
            }
            for t in treatments
        ]

        doctors = session.query(Doctor, User).join(
            User, Doctor.uid == User.id
        ).all()

        doctors_list = [
            {
                "id": d.id,
                "name": u.name
            }
            for d, u in doctors
        ]

        patients = session.query(Patient, User).join(
            User, Patient.uid == User.id
        ).all()

        patients_list = [
            {
                "id": p.id,
                "name": u.name
            }
            for p, u in patients
        ]

        return jsonify({
            "success": True,
            "treatments": treatments_list,
            "filters": {
                "doctor_id": filter_doctor,
                "patient_id": filter_patient
            },
            "doctors": doctors_list,
            "patients": patients_list
        }), 200

    except Exception as e:
        print(f"[ERROR] Admin treatments: {e}")

        return jsonify({
            "success": False,
            "message": "Error loading treatments"
        }), 500

    finally:
        session.close()

@app.route("/api/doctor/appointments", methods=["GET"])
@login_required
def doctor_appointments():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        today = date.today()
        next_week = today + timedelta(days=7)

        filter_option = request.args.get("filter", "all")

        query = session.query(Appointment).join(
            Patient, Appointment.patid == Patient.id
        ).filter(
            Appointment.docid == doctor.id
        )

        if filter_option == "today":
            query = query.filter(Appointment.appoint_date == today)
        elif filter_option == "upcoming":
            query = query.filter(Appointment.appoint_date.between(today, next_week))

        appointments_query = query.order_by(
            Appointment.appoint_date.asc(),
            Appointment.appoint_time.asc()
        ).all()

        appointments = []

        for appt in appointments_query:
            patient = appt.patient
            user = patient.user if patient else None

            age = 0
            if patient and patient.dob:
                today_date = date.today()
                age = today_date.year - patient.dob.year - (
                    (today_date.month, today_date.day) < (patient.dob.month, patient.dob.day)
                )

            appointments.append({
                "id": appt.id,
                "appointment_number": appt.appointment_number,
                "appointment_date": appt.appoint_date.strftime("%Y-%m-%d") if appt.appoint_date else None,
                "appointment_time": appt.appoint_time.strftime("%H:%M") if appt.appoint_time else None,
                "status": appt.status,
                "reason": appt.reason_for_visit or "",
                "patient": {
                    "name": user.name if user else "Unknown",
                    "gender": patient.gender if patient else "-",
                    "age": age,
                    "blood_group": patient.blood_group if patient else "-",
                    "address": patient.address if patient else "-"
                }
            })

        total_appointments = len(appointments)

        todays_appointments = sum(
            1 for a in appointments if a["appointment_date"] == today.strftime("%Y-%m-%d")
        )

        upcoming_appointments = sum(
            1 for a in appointments
            if a["appointment_date"]
            and today.strftime("%Y-%m-%d") <= a["appointment_date"] <= next_week.strftime("%Y-%m-%d")
            and a["status"] == "Booked"
        )

        return jsonify({
            "success": True,
            "appointments": appointments,
            "stats": {
                "total": total_appointments,
                "today": todays_appointments,
                "upcoming": upcoming_appointments
            },
            "filter": filter_option
        }), 200

    except Exception as e:
        print("[ERROR] doctor_appointments:", e)

        return jsonify({
            "success": False,
            "message": "Error loading appointments"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/appointments/<int:appointment_id>", methods=["GET"])
@login_required
def doctor_view_appointment(appointment_id):

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            docid=doctor.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        patient = appointment.patient
        user = patient.user if patient else None

        treatment = session.query(Treatment).filter_by(
            appointid=appointment.id
        ).first()

        age = 0
        if patient and patient.dob:
            today_date = date.today()
            age = today_date.year - patient.dob.year - (
                (today_date.month, today_date.day) < (patient.dob.month, patient.dob.day)
            )

        return jsonify({
            "success": True,
            "appointment": {
                "id": appointment.id,
                "appointment_number": appointment.appointment_number,
                "date": appointment.appoint_date.strftime("%Y-%m-%d") if appointment.appoint_date else None,
                "time": appointment.appoint_time.strftime("%H:%M") if appointment.appoint_time else None,
                "status": appointment.status,
                "reason": appointment.reason_for_visit or ""
            },
            "patient": {
                "name": user.name if user else "Unknown",
                "gender": patient.gender if patient else "-",
                "age": age,
                "blood_group": patient.blood_group if patient else "-",
                "address": patient.address if patient else "-"
            },
            "treatment": {
                "diagnosis": treatment.diagnosis if treatment else None,
                "prescription": treatment.prescription if treatment else None,
                "notes": treatment.notes if treatment else None
            }
        }), 200

    except Exception as e:
        print("[ERROR] doctor_view_appointment:", e)

        return jsonify({
            "success": False,
            "message": "Error loading appointment details"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/appointments/<int:appointment_id>/complete", methods=["PUT"])
@login_required
def doctor_mark_complete(appointment_id):

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            docid=doctor.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        if appointment.status != "Booked":
            return jsonify({
                "success": False,
                "message": "Only booked appointments can be marked complete"
            }), 400

        appointment.status = "Completed"
        session.commit()

        return jsonify({
            "success": True,
            "message": "Appointment marked as completed"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] doctor_mark_complete:", e)

        return jsonify({
            "success": False,
            "message": "Error updating appointment"
        }), 500

    finally:
        session.close()

@app.route("/api/doctor/appointments/<int:appointment_id>/cancel", methods=["PUT"])
@login_required
def doctor_mark_cancel(appointment_id):

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            docid=doctor.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        if appointment.status != "Booked":
            return jsonify({
                "success": False,
                "message": "Only booked appointments can be cancelled"
            }), 400

        appointment.status = "Cancelled"
        session.commit()

        return jsonify({
            "success": True,
            "message": "Appointment cancelled successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] doctor_mark_cancel:", e)

        return jsonify({
            "success": False,
            "message": "Error cancelling appointment"
        }), 500

    finally:
        session.close()

@app.route("/api/doctor/appointments/<int:appointment_id>/diagnose", methods=["POST"])
@login_required
def doctor_diagnose(appointment_id):

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        appointment = session.query(Appointment).filter_by(
            id=appointment_id,
            docid=doctor.id
        ).first()

        if not appointment:
            return jsonify({
                "success": False,
                "message": "Appointment not found"
            }), 404

        data = request.get_json()

        diagnosis = data.get("diagnosis")
        treatment_plan = data.get("treatment_plan")
        prescription = data.get("prescription")
        notes = data.get("notes")
        next_visit_str = data.get("next_visit_date")

        next_visit_date = None
        if next_visit_str:
            try:
                next_visit_date = datetime.strptime(next_visit_str, "%Y-%m-%d").date()
            except:
                return jsonify({
                    "success": False,
                    "message": "Invalid date format"
                }), 400

        patient_id = appointment.patid

        treatment = session.query(Treatment).filter_by(
            appointid=appointment.id
        ).first()

        medical_history = session.query(MedicalHistory).filter_by(
            patid=patient_id
        ).first()

        if treatment:
            treatment.diagnosis = diagnosis
            treatment.treatment_plan = treatment_plan
            treatment.prescription = prescription
            treatment.notes = notes
            treatment.next_visit_date = next_visit_date
        else:
            treatment = Treatment(
                appointid=appointment.id,
                docid=appointment.docid,
                patid=patient_id,
                diagnosis=diagnosis,
                treatment_plan=treatment_plan,
                prescription=prescription,
                notes=notes,
                next_visit_date=next_visit_date
            )
            session.add(treatment)

        timestamp = datetime.now().strftime('%Y-%m-%d')

        if medical_history:
            if diagnosis:
                if medical_history.chronic_conditions:
                    medical_history.chronic_conditions += f"\n[{timestamp}] {diagnosis}"
                else:
                    medical_history.chronic_conditions = f"[{timestamp}] {diagnosis}"

            if prescription:
                if medical_history.current_medications:
                    medical_history.current_medications += f"\n[{timestamp}] {prescription}"
                else:
                    medical_history.current_medications = f"[{timestamp}] {prescription}"
        else:
            medical_history = MedicalHistory(
                patid=patient_id,
                chronic_conditions=f"[{timestamp}] {diagnosis}" if diagnosis else None,
                current_medications=f"[{timestamp}] {prescription}" if prescription else None
            )
            session.add(medical_history)

        appointment.status = "Completed"

        session.commit()

        return jsonify({
            "success": True,
            "message": "Diagnosis saved successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] doctor_diagnose:", e)

        return jsonify({
            "success": False,
            "message": "Error saving treatment"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/patients", methods=["GET"])
@login_required
def doctor_patients():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        patients_query = (
            session.query(Patient)
            .join(Appointment, Appointment.patid == Patient.id)
            .filter(Appointment.docid == doctor.id)
            .group_by(Patient.id)
            .all()
        )

        patients_list = []

        for patient in patients_query:
            age = 0
            if patient.dob:
                today_date = date.today()
                age = today_date.year - patient.dob.year - (
                    (today_date.month, today_date.day) < (patient.dob.month, patient.dob.day)
                )

            appointment_count = session.query(Appointment).filter(
                Appointment.patid == patient.id,
                Appointment.docid == doctor.id
            ).count()

            last_visit = session.query(Appointment.appoint_date).filter(
                Appointment.patid == patient.id,
                Appointment.docid == doctor.id
            ).order_by(
                Appointment.appoint_date.desc()
            ).first()

            patients_list.append({
                "id": patient.id,
                "name": patient.user.name if patient.user else "",
                "gender": patient.gender,
                "age": age,
                "blood_group": patient.blood_group,
                "address": patient.address,
                "appointment_count": appointment_count,
                "last_visit": last_visit[0].strftime("%Y-%m-%d") if last_visit else None
            })

        return jsonify({
            "success": True,
            "patients": patients_list
        }), 200

    except Exception as e:
        print("[ERROR] doctor_patients:", e)

        return jsonify({
            "success": False,
            "message": "Error loading patients"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/availability", methods=["GET"])
@login_required
def get_doctor_availability():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        today = date.today()
        availability_data = []

        for day_index in range(7):
            current_date = today + timedelta(days=day_index)

            availability = session.query(DoctorAvailability).filter_by(
                docid=doctor.id,
                available_date=current_date
            ).first()

            availability_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_name": current_date.strftime("%A"),
                "available": availability.available if availability else False,
                "start_time": availability.start_time.strftime("%H:%M") if availability and availability.start_time else None,
                "end_time": availability.end_time.strftime("%H:%M") if availability and availability.end_time else None
            })

        return jsonify({
            "success": True,
            "availability": availability_data
        }), 200

    except Exception as e:
        print("[ERROR] get_doctor_availability:", e)

        return jsonify({
            "success": False,
            "message": "Error loading availability"
        }), 500

    finally:
        session.close()

@app.route("/api/doctor/availability", methods=["POST"])
@login_required
def update_doctor_availability():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        data = request.get_json()
        availability_list = data.get("availability", [])

        for item in availability_list:
            date_str = item.get("date")
            available = item.get("available", False)
            start_time_str = item.get("start_time")
            end_time_str = item.get("end_time")

            current_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            availability = session.query(DoctorAvailability).filter_by(
                docid=doctor.id,
                available_date=current_date
            ).first()

            if available and start_time_str and end_time_str:
                start_time = datetime.strptime(start_time_str, "%H:%M").time()
                end_time = datetime.strptime(end_time_str, "%H:%M").time()

                if availability:
                    availability.available = True
                    availability.start_time = start_time
                    availability.end_time = end_time
                else:
                    availability = DoctorAvailability(
                        docid=doctor.id,
                        available_date=current_date,
                        start_time=start_time,
                        end_time=end_time,
                        available=True
                    )
                    session.add(availability)
            else:
                if availability:
                    availability.available = False

        session.commit()

        return jsonify({
            "success": True,
            "message": "Availability updated successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] update_doctor_availability:", e)

        return jsonify({
            "success": False,
            "message": "Error updating availability"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/treatments", methods=["GET"])
@login_required
def doctor_treatments():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        treatments_query = (
            session.query(Treatment)
            .join(Appointment, Treatment.appointid == Appointment.id)
            .join(Patient, Treatment.patid == Patient.id)
            .filter(Treatment.docid == doctor.id)
            .order_by(Treatment.treatment_date.desc())
            .all()
        )

        treatments_list = [
            {
                "id": t.id,
                "patient_name": t.patient.user.name if t.patient and t.patient.user else "N/A",
                "diagnosis": t.diagnosis or "",
                "treatment_plan": t.treatment_plan or "",
                "prescription": t.prescription or "",
                "notes": t.notes or "",
                "treatment_date": t.treatment_date.strftime("%Y-%m-%d") if t.treatment_date else None,
                "appointment_date": t.appointment.appoint_date.strftime("%Y-%m-%d") if t.appointment and t.appointment.appoint_date else None,
                "next_visit_date": t.next_visit_date.strftime("%Y-%m-%d") if t.next_visit_date else None
            }
            for t in treatments_query
        ]

        return jsonify({
            "success": True,
            "treatments": treatments_list
        }), 200

    except Exception as e:
        print("[ERROR] doctor_treatments:", e)

        return jsonify({
            "success": False,
            "message": "Error loading treatments"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/patients/<int:patient_id>/history", methods=["GET"])
@login_required
def doctor_patient_history(patient_id):

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        patient = session.query(Patient).filter_by(id=patient_id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient not found"
            }), 404

        medical_history = session.query(MedicalHistory).filter_by(
            patid=patient_id
        ).first()

        treatments = (
            session.query(Treatment)
            .join(Appointment, Treatment.appointid == Appointment.id)
            .filter(
                Treatment.patid == patient_id,
                Treatment.docid == doctor.id
            )
            .order_by(Treatment.treatment_date.desc())
            .all()
        )

        appointments = (
            session.query(Appointment)
            .filter(
                Appointment.patid == patient_id,
                Appointment.docid == doctor.id
            )
            .order_by(Appointment.appoint_date.desc())
            .all()
        )

        age = 0
        if patient.dob:
            today_date = date.today()
            age = today_date.year - patient.dob.year - (
                (today_date.month, today_date.day) < (patient.dob.month, patient.dob.day)
            )

        treatments_list = [
            {
                "id": t.id,
                "date": t.treatment_date.strftime("%Y-%m-%d") if t.treatment_date else None,
                "diagnosis": t.diagnosis or "",
                "prescription": t.prescription or "",
                "notes": t.notes or ""
            }
            for t in treatments
        ]

        appointments_list = [
            {
                "id": a.id,
                "date": a.appoint_date.strftime("%Y-%m-%d") if a.appoint_date else None,
                "time": a.appoint_time.strftime("%H:%M") if a.appoint_time else None,
                "status": a.status,
                "reason": a.reason_for_visit or ""
            }
            for a in appointments
        ]

        return jsonify({
            "success": True,
            "patient": {
                "id": patient.id,
                "name": patient.user.name if patient.user else "",
                "gender": patient.gender,
                "age": age,
                "blood_group": patient.blood_group,
                "address": patient.address
            },
            "medical_history": {
                "allergies": medical_history.allergies if medical_history else "",
                "chronic_conditions": medical_history.chronic_conditions if medical_history else "",
                "medications": medical_history.current_medications if medical_history else "",
                "notes": medical_history.notes if medical_history else ""
            },
            "treatments": treatments_list,
            "appointments": appointments_list
        }), 200

    except Exception as e:
        print("[ERROR] doctor_patient_history:", e)

        return jsonify({
            "success": False,
            "message": "Error loading patient history"
        }), 500

    finally:
        session.close()


@app.route("/api/doctor/profile", methods=["GET"])
@login_required
def get_doctor_profile():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        user = session.query(User).filter_by(id=current_user.id).first()

        department = session.query(Department).filter_by(
            id=doctor.depid
        ).first() if doctor.depid else None

        total_appointments = session.query(Appointment).filter(
            Appointment.docid == doctor.id
        ).count()

        completed_appointments = session.query(Appointment).filter(
            Appointment.docid == doctor.id,
            Appointment.status == "Completed"
        ).count()

        total_patients = session.query(Patient).join(
            Appointment, Appointment.patid == Patient.id
        ).filter(
            Appointment.docid == doctor.id
        ).group_by(Patient.id).count()

        return jsonify({
            "success": True,
            "profile": {
                "name": user.name if user else "",
                "specialization": doctor.specialization,
                "qualification": doctor.qualification,
                "experience": doctor.experience,
                "gender": doctor.gender,
                "department": department.name if department else None
            },
            "stats": {
                "total_appointments": total_appointments,
                "completed_appointments": completed_appointments,
                "total_patients": total_patients
            }
        }), 200

    except Exception as e:
        print("[ERROR] get_doctor_profile:", e)

        return jsonify({
            "success": False,
            "message": "Error loading profile"
        }), 500

    finally:
        session.close()

@app.route("/api/doctor/profile", methods=["PUT"])
@login_required
def update_doctor_profile():

    if current_user.role != "doctor":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        doctor = session.query(Doctor).filter_by(uid=current_user.id).first()

        if not doctor:
            return jsonify({
                "success": False,
                "message": "Doctor profile not found"
            }), 404

        user = session.query(User).filter_by(id=current_user.id).first()

        name = data.get("name")
        specialization = data.get("specialization")
        qualification = data.get("qualification")
        experience = data.get("experience")
        gender = data.get("gender")

        if name and user:
            user.name = name

        if specialization:
            doctor.specialization = specialization

        if qualification:
            doctor.qualification = qualification

        if experience is not None:
            try:
                exp_val = int(experience)
                if exp_val < 0:
                    return jsonify({
                        "success": False,
                        "message": "Experience cannot be negative"
                    }), 400
                doctor.experience = exp_val
            except:
                return jsonify({
                    "success": False,
                    "message": "Invalid experience value"
                }), 400

        if gender:
            doctor.gender = gender

        session.commit()

        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] update_doctor_profile:", e)

        return jsonify({
            "success": False,
            "message": "Error updating profile"
        }), 500

    finally:
        session.close()

@app.route("/api/patient/profile", methods=["GET"])
@login_required
def get_patient_profile():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        user = session.query(User).filter_by(id=current_user.id).first()

        return jsonify({
            "success": True,
            "profile": {
                "name": user.name if user else "",
                "gender": patient.gender,
                "dob": patient.dob.strftime("%Y-%m-%d") if patient.dob else None,
                "blood_group": patient.blood_group,
                "address": patient.address
            }
        }), 200

    except Exception as e:
        print("[ERROR] get_patient_profile:", e)

        return jsonify({
            "success": False,
            "message": "Error loading profile"
        }), 500

    finally:
        session.close()

@app.route("/api/patient/profile", methods=["PUT"])
@login_required
def update_patient_profile():

    if current_user.role != "patient":
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    session = SessionLocal()

    try:
        data = request.get_json()

        patient = session.query(Patient).filter_by(uid=current_user.id).first()

        if not patient:
            return jsonify({
                "success": False,
                "message": "Patient profile not found"
            }), 404

        gender = data.get("gender")
        dob_str = data.get("dob")
        blood_group = data.get("blood_group")
        address = data.get("address")
        name = data.get("name")

        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except:
                return jsonify({
                    "success": False,
                    "message": "Invalid date format"
                }), 400

        user = session.query(User).filter_by(id=current_user.id).first()

        if name and user:
            user.name = name

        if gender:
            patient.gender = gender

        if dob is not None:
            patient.dob = dob

        if blood_group:
            patient.blood_group = blood_group

        if address:
            patient.address = address

        session.commit()

        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200

    except Exception as e:
        session.rollback()
        print("[ERROR] update_patient_profile:", e)

        return jsonify({
            "success": False,
            "message": "Error updating profile"
        }), 500

    finally:
        session.close()

# --- Initialization ---
def initialize_app():
    Base.metadata.create_all(engine)
    create_super_admin()
    create_standard_departments()


if __name__ == "__main__":
    initialize_app()
    app.run(debug=True)