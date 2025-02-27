from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Correct initialization of Flask app
app = Flask(__name__) 
app.secret_key = 'e7a4387f0156601592bee3eac6cdaf2c'  # Required for flashing messages

# Email configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'pashalawsenate@gmail.com'  # Replace with your Gmail
EMAIL_PASSWORD = 'jecz taxe ucnn okkx'  # Use Gmail App Password

def send_email(name, email, message):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = 'ebrahimrafeeq@gmail.com'  # Replace with receiver email
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

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    # Pass the datetime module to the template
    return render_template('index.html', datetime=datetime)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if send_email(name, email, message):
        flash('Thank you! Your inquiry has been received.', 'success')
    else:
        flash('Failed to send your inquiry. Please try again.', 'error')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug= True)
    app.run(host='0.0.0.0', port=5000)