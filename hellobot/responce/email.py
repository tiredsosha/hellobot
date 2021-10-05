import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Send:
    def __init__(self, admin, password, server, port):
        self.admin = admin
        self.password = password
        self.server = server
        self.port = port

    def start(self):
        server = smtplib.SMTP(self.server, self.port)
        server.starttls()
        server.login(self.admin, self.password)
        return server

    def message(self):
        msg = MIMEMultipart()
        msg['From'] = self.admin
        msg['Subject'] = 'HelloBot is saying hi!'
        return msg

    #@staticmethod
    async def send(self, body, user):
        msg = self.message()
        server = self.start()
        msg['To'] = user
        msg.attach(MIMEText(body))
        server.send_message(msg)
        server.quit()
