import smtplib
import asyncio
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Send:
    def __init__(self):
        self.admin = 'soshapinger@gmail.com'
        self.password = 'qwertyty5477'
        self.server = 'smtp.gmail.com'
        self.port = 587
        self.handle = None
        self.start()

    def start(self):
        print(self.admin, self.password)
        server = smtplib.SMTP(self.server, self.port)
        server.starttls()
        server.login(self.admin, self.password)
        self.handle = server

    def message(self):
        msg = MIMEMultipart()
        msg['From'] = self.admin
        msg['Subject'] = 'HelloBot is saying hi!'
        return msg

    async def send(self, body, user):
        msg = self.message()
        msg['To'] = user
        msg.attach(MIMEText(body))
        self.handle.send_message(msg)


m = Send()

while True:
    asyncio.run(m.send('dddddddddd', 'sasha.che007@gmail.com'))
    asyncio.run(m.send('dddddddddd', 'a.chichko@hello.io'))
    print('here')
    time.sleep(10)
