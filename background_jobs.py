import os
import smtplib
import csv
import io
from datetime import datetime, date, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import requests

from celery import Celery

from app import SessionLocal, User, Patient, Doctor, Appointment, Treatment


GCHAT_WEBHOOK_URL = os.environ.get('GCHAT_WEBHOOK_URL', '')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
FROM_EMAIL = os.environ.get('FROM_EMAIL', SMTP_USERNAME)

celery_app = Celery(
    'hospital_jobs',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

celery_app.conf.update(
    beat_schedule={
        'daily-reminders': {
            'task': 'background_jobs.send_daily_reminders',
            'schedule': 86400.0,
        },
        'monthly-report': {
            'task': 'background_jobs.generate_monthly_reports',
            'schedule': 2592000.0,
        },
    },
    timezone='UTC',
)


def send_email(to_email, subject, body, attachments=None):
    """Send email with optional attachments"""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("[EMAIL] SMTP not configured, skipping email")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        if attachments:
            for filename, content in attachments.items():
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(content)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[EMAIL] Sent to {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL] Failed to send email: {e}")
        return False


def send_google_chat_message(webhook_url, message):
    """Send message to Google Chat using webhook"""
    if not webhook_url:
        print("[GCHAT] Webhook URL not configured")
        return False
    
    try:
        payload = {
            "text": message
        }
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"[GCHAT] Failed to send message: {e}")
        return False


@celery_app.task(name='background_jobs.send_daily_reminders')
def send_daily_reminders():
    """Send daily reminders to patients with appointments today"""
    print(f"[JOB] Running daily reminders at {datetime.now()}")
    
    session = SessionLocal()
    try:
        today = date.today()
        
        appointments = session.query(Appointment, User, Doctor, User).join(
            Patient, Appointment.patid == Patient.id
        ).join(
            User, Patient.uid == User.id
        ).join(
            Doctor, Appointment.docid == Doctor.id
        ).join(
            User, Doctor.uid == User.id
        ).filter(
            Appointment.appoint_date == today,
            Appointment.status == 'Booked'
        ).all()
        
        if not appointments:
            print("[JOB] No appointments today")
            return "No appointments"
        
        for apt, patient_user, doctor, doctor_user in appointments:
            patient_name = patient_user.name
            doctor_name = doctor_user.name
            appointment_time = apt.appoint_time.strftime("%H:%M") if apt.appoint_time else "N/A"
            reason = apt.reason_for_visit or "General checkup"
            
            message = f"""
Hospital Appointment Reminder

Hello {patient_name},

This is a reminder about your appointment today:
- Doctor: Dr. {doctor_name}
- Time: {appointment_time}
- Reason: {reason}

Please arrive 15 minutes early.

Thank you!
"""
            email = patient_user.email or patient_user.username
            if email:
                send_email(
                    email,
                    "Hospital Appointment Reminder",
                    f"<html><body><pre>{message}</pre></body></html>"
                )
            
            if GCHAT_WEBHOOK_URL:
                send_google_chat_message(GCHAT_WEBHOOK_URL, message)
        
        print(f"[JOB] Sent {len(appointments)} reminders")
        return f"Sent {len(appointments)} reminders"
        
    except Exception as e:
        print(f"[JOB] Error sending reminders: {e}")
        return str(e)
    finally:
        session.close()


@celery_app.task(name='background_jobs.generate_monthly_reports')
def generate_monthly_reports():
    """Generate monthly activity report for all doctors"""
    print(f"[JOB] Generating monthly reports at {datetime.now()}")
    
    session = SessionLocal()
    try:
        today = date.today()
        first_day = today.replace(day=1)
        last_month = first_day - timedelta(days=1)
        month_start = last_month.replace(day=1)
        
        doctors = session.query(Doctor).all()
        
        for doctor in doctors:
            doctor_user = session.query(User).filter_by(id=doctor.uid).first()
            if not doctor_user or not doctor_user.email:
                continue
            
            doctor_name = doctor_user.name
            
            appointments = session.query(Appointment).filter(
                Appointment.docid == doctor.id,
                Appointment.appoint_date >= month_start,
                Appointment.appoint_date < first_day,
                Appointment.status.in_(['Completed', 'Booked'])
            ).all()
            
            completed = session.query(Appointment).filter(
                Appointment.docid == doctor.id,
                Appointment.appoint_date >= month_start,
                Appointment.appoint_date < first_day,
                Appointment.status == 'Completed'
            ).count()
            
            treatments = session.query(Treatment).join(Appointment).filter(
                Appointment.docid == doctor.id,
                Appointment.appoint_date >= month_start,
                Appointment.appoint_date < first_day
            ).all()
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        .summary {{ background-color: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Monthly Activity Report</h1>
    <p>Period: {month_start.strftime('%B %Y')}</p>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    
    <div class="summary">
        <h2>Dr. {doctor_name}</h2>
        <p><strong>Specialization:</strong> {doctor.specialization or 'General'}</p>
        <p><strong>Total Appointments:</strong> {len(appointments)}</p>
        <p><strong>Completed:</strong> {completed}</p>
        <p><strong>Treatments Given:</strong> {len(treatments)}</p>
    </div>
    
    <h3>Appointment Details</h3>
    <table>
        <tr>
            <th>Date</th>
            <th>Patient</th>
            <th>Status</th>
            <th>Diagnosis</th>
            <th>Treatment</th>
        </tr>
"""
            
            for apt in appointments:
                patient = session.query(Patient).filter_by(id=apt.patid).first()
                patient_user = session.query(User).filter_by(id=patient.uid).first() if patient else None
                patient_name = patient_user.name if patient_user else "Unknown"
                
                treatment = session.query(Treatment).filter_by(appointid=apt.id).first()
                diagnosis = treatment.diagnosis if treatment else "N/A"
                treatment_plan = treatment.treatment_plan if treatment else "N/A"
                
                html_content += f"""
        <tr>
            <td>{apt.appoint_date.strftime('%Y-%m-%d') if apt.appoint_date else 'N/A'}</td>
            <td>{patient_name}</td>
            <td>{apt.status}</td>
            <td>{diagnosis}</td>
            <td>{treatment_plan}</td>
        </tr>
"""
            
            html_content += """
    </table>
</body>
</html>
"""
            
            send_email(
                doctor_user.email,
                f"Monthly Activity Report - {month_start.strftime('%B %Y')}",
                html_content
            )
        
        print(f"[JOB] Generated reports for {len(doctors)} doctors")
        return f"Generated reports for {len(doctors)} doctors"
        
    except Exception as e:
        print(f"[JOB] Error generating reports: {e}")
        return str(e)
    finally:
        session.close()


@celery_app.task(name='background_jobs.export_treatment_csv')
def export_treatment_csv(patient_id):
    """Export patient treatment history as CSV"""
    print(f"[JOB] Exporting treatment CSV for patient {patient_id}")
    
    session = SessionLocal()
    try:
        patient = session.query(Patient).filter_by(id=patient_id).first()
        if not patient:
            return None
        
        patient_user = session.query(User).filter_by(id=patient.uid).first()
        
        treatments = session.query(Treatment, Appointment, User, User).join(
            Appointment, Treatment.appointid == Appointment.id
        ).join(
            User, Appointment.patid == User.id
        ).join(
            Doctor, Treatment.docid == Doctor.id
        ).join(
            User, Doctor.uid == User.id
        ).filter(
            Appointment.patid == patient_id
        ).order_by(Appointment.appoint_date.desc()).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'User ID', 'Username', 'Consulting Doctor', 'Appointment Date',
            'Diagnosis', 'Treatment', 'Prescription', 'Notes', 'Next Visit'
        ])
        
        for treatment, appointment, pat_user, doc_user in treatments:
            writer.writerow([
                patient.id,
                patient_user.username if patient_user else 'N/A',
                doc_user.name if doc_user else 'N/A',
                appointment.appoint_date.strftime('%Y-%m-%d') if appointment.appoint_date else 'N/A',
                treatment.diagnosis or 'N/A',
                treatment.treatment_plan or 'N/A',
                treatment.prescription or 'N/A',
                treatment.notes or 'N/A',
                treatment.next_visit_date.strftime('%Y-%m-%d') if treatment.next_visit_date else 'N/A'
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        patient_email = patient_user.email if patient_user else None
        if patient_email:
            send_email(
                patient_email,
                "Your Treatment History Export",
                "Please find attached your treatment history.",
                attachments={f'treatment_history_{datetime.now().strftime("%Y%m%d")}.csv': csv_content}
            )
        
        return csv_content
        
    except Exception as e:
        print(f"[JOB] Error exporting CSV: {e}")
        return str(e)
    finally:
        session.close()


if __name__ == '__main__':
    celery_app.start()
