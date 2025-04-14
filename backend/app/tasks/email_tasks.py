from celery import Celery
from flask_mail import Mail, Message
from flask import render_template
from models.user import User,db, ServiceRequest
from sqlalchemy import func
from datetime import datetime
from celery import shared_task
import csv
import uuid

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = '21f3000500@study.iitm.ac.in'
SENDER_PASSWORD = ''


def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()




@shared_task(ignore_result=True)
def daily_reminder(email, subject):
    subject = "Daily Reminder"
    #today = datetime.now().date()
    user_emails = db.session.query(User.email).filter(User.role =="professional").all()
    
    print(user_emails)

    for email in user_emails:
        #with open('templates/usr_reminder_email_temp.html', 'r') as f:
            
           
       send_message(to=email[0], subject=subject,content_body="mer ")

    return "Daily reminder sent"


@shared_task(ignore_result=True)
def notify_professionals_of_pending_requests():
   # Query for service requests with status 'requested'
   requested_services = db.session.query(ServiceRequest).filter_by(service_status='requested').all()
   for request in requested_services:
       # Get the professional's email using professional_id
       professional = db.session.query(User).get(request.professional_id)
       
       if professional and professional.email:
           # Prepare the email content
           subject = "New Service Request Notification"
           body = f"Dear {professional.fullname},\n\nYou have a new service request pending. Please visit your dashboard to accept or reject the request.\n\nThank you."
           
           # Send the email
           send_message(professional.email, subject, body)
   return "Emails sent to professionals with pending requests."




@shared_task(ignore_result=True)
def send_monthly_activity_reports():
    # Fetch all users
    users = db.session.query(User).filter(User.role == 'customer').all()

    for user in users:
        # Get the requested and closed counts for the user
        counts = get_requested_and_closed_counts(user.id)

        # Render the email content using the template
        email_content = render_template(
            'monthly_report.html',
            requested=counts.get('requested', 0),
            closed=counts.get('closed', 0)
        )

        # Send the email
        send_message(
            to=user.email,
            subject="Your Monthly Activity Report",
            content_body=email_content
        )

    return "Monthly activity reports sent to all users."





def get_requested_and_closed_counts(user_id):
    # Query to count 'requested' and 'closed' service requests for the given user ID
    counts = db.session.query(
        ServiceRequest.service_status,
        func.count(ServiceRequest.id)
    ).filter(
        ServiceRequest.customer_id == user_id,
        ServiceRequest.service_status.in_(['requested', 'closed'])
    ).group_by(
        ServiceRequest.service_status
    ).all()

    # Initialize the result dictionary with default counts
    result = {'requested': 0, 'closed': 0}

    # Update the result dictionary with actual counts from the query
    for status, count in counts:
        result[status] = count

    return result

''' 
@shared_task
def export_all_service_requests(admin_email):
    """
    Celery task to export all service requests to a CSV file.
    Sends an email notification once done.
    """
    # Query all service requests
    all_requests = db.session.query(
        ServiceRequest.service_id,
        ServiceRequest.customer_id,
        ServiceRequest.professional_id,
        ServiceRequest.date_of_request,
        ServiceRequest.service_status,
        
    ).all()

    # File path for the CSV export
    file_path = "admin_trigerred_service_requests.csv"

    # Write data to CSV
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Service ID", "Customer ID", "Professional ID", "Date of Request", "Status"])
        writer.writerows(all_requests)

    # Send email to notify admin
    send_message(
        subject="Service Requests Export Completed",
        recipient="admin@example.com",
        html_content=f"The export of all service requests is completed. File is available at: {file_path}"
    )

    return f"Export completed and saved at {file_path}."

'''


@shared_task
def export_all_service_requests():
    """
    Celery task to export all service requests to a CSV file.
    The file will be saved with a unique name to prevent overwriting.
    """
    # Query all service requests
    all_requests = db.session.query(
        ServiceRequest.service_id,
        ServiceRequest.customer_id,
        ServiceRequest.professional_id,
        ServiceRequest.date_of_request,
        ServiceRequest.service_status,
    ).all()

    # Create a unique file name using timestamp and UUID
    unique_id = uuid.uuid4()  # Generate a unique identifier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Use the current timestamp for uniqueness
    file_name = f"service_requests_export_{timestamp}_{unique_id}.csv"
    
    # File path for the CSV export (ensure to save it in an appropriate directory)
    file_path = f"./static/{file_name}"  # Save it in the 'exports' folder or any desired directory

    # Write data to CSV
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Service ID", "Customer ID", "Professional ID", "Date of Request", "Status"])
        writer.writerows(all_requests)

    return file_path



