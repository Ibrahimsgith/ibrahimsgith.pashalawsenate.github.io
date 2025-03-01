from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Context processor to inject datetime for templates
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

# Secret key for sessions (use environment variable in production)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'e7a4387f0156601592bee3eac6cdaf2c')

# Email configuration (use environment variables for security)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = os.environ.get('EMAIL_USER', 'pashalawsenate@gmail.com')  # Replace or use env var
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'jecz taxe ucnn okkx')  # Use Gmail App Password or env var

def send_email(name, email, message):
    """
    Send an email with the contact form details.
    Returns True if successful, False otherwise.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = os.environ.get('RECEIVER_EMAIL', 'ebrahimrafeeq@gmail.com')  # Use env var or default
        msg['Subject'] = f"New Inquiry from {name}"

        body = f"""
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Message:</strong><br>{message}</p>
        """
        msg.attach(MIMEText(body, 'html'))

        # Send the email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, msg['To'], msg.as_string())

        print(f"Email sent successfully to {msg['To']}")
        return True
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    logger.debug(f"Request method: {request.method}")
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):  # Basic validation
            flash('All fields are required. Please try again.', 'error')
            return redirect(url_for('contact'))

        if send_email(name, email, message):
            flash('Thank you! Your inquiry has been received.', 'success')
        else:
            flash('Failed to send your inquiry. Please try again.', 'error')

        return redirect(url_for('home'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)