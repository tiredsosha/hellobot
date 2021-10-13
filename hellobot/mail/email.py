import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Send:
    def __init__(self, admin, password, server, port):
        self.admin = admin
        self.password = password
        self.server = server
        self.port = port
        self.handle = None
        self.start()

    def start(self):
        server = smtplib.SMTP(self.server, self.port)
        server.starttls()
        server.login(self.admin, self.password)
        self.handle = server

    def message(self):
        msg = MIMEMultipart()
        msg['From'] = self.admin
        msg['Subject'] = 'HelloBot is saying hi!'
        return msg

    def send(self, body, user):
        msg = self.message()
        msg['To'] = user
        msg.attach(MIMEText(body))
        self.handle.send_message(msg)
