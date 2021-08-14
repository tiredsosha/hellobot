import os
import smtplib
from pathlib import Path
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Email:

    def __init__(self, send_to, body_email, send_from=os.environ['sender_email'], password=os.environ['sender_password'], server_adress='smtp.gmail.com', server_port=587):

        self.to = send_to
        self.body = body_email
        self.from = send_from
        self.password = password
        self.adress = server_adress
        self.port = server_port


    def create_email(self):
        msg = MIMEMultipart()
        msg['From']    = self.from
        msg['To']      = self.to
        msg['Subject'] = 'Твой пароль от пассворка'
        body = self.body
        return msg.attach(MIMEText(body))


    def send_email(self):
        server = smtplib.SMTP(self.adress, self.port)
        server.starttls()
        server.login(self.from, self.password)
        server.send_message(self.create_email())
        server.quit()
