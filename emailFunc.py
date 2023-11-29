import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()
GMAIL_EMAIL=os.getenv('GMAIL_EMAIL')
GMAIL_PASSWORD= os.getenv('GMAIL_PASSWORD')
def send_email(receiver_email:str, subject:str, body:str)-> None:  
    """
    This function helps to send an email to the user
    :param receiver_email: email of the receiver
    :param subject: subject of the email
    :param body: body of the email
    :return: None
    """
    sender_email = GMAIL_EMAIL
    password = GMAIL_PASSWORD  # For Gmail, use an app-specific password
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, 'plain'))

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender_email, password)
    smtp_server.send_message(message)
    smtp_server.quit()