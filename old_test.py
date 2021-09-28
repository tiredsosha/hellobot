#!/usr/bin/python3

from asyncio import events
from typing import Text
import slack
import os
import paramiko
import re
import smtplib
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# make server that lisens to slack events
app = Flask(__name__)
slack_event_handler = SlackEventAdapter(os.environ['slack_singing'], '/slack/events', app)

# email function
def email_passcode(to, ebody):
    addr_from = os.environ['admin_email']
    password  = os.environ['admin_password']
    msg = MIMEMultipart()
    msg['From']    = addr_from
    msg['To']      = to
    msg['Subject'] = 'Твой пароль от пассворка'
    body = ebody
    msg.attach(MIMEText(body))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()

master_pass = os.environ['master_pass']
print(os.environ['admin_email'])

# default responce for passwork
def passwork_responce(email, dep_value, user_id, master=master_pass):
    client.chat_postMessage(channel=f'{user_id}', text="\nжди письмеца c парольчиком на почте\nпока-пока")
    email_passcode(email, f'login: {dictionary.get(dep_value, None)[0]}\npassword: {dictionary.get(dep_value, None)[1]}\nмастер пароль: {master}\n\n\n\n\n\n\nShRaK')
    now = datetime.now()
    print(dep_value, now)

# Open a transport
host, port = ".ftp.ihc.ru", 22
transport = paramiko.Transport((host, port))
username, password = "", ""
transport.connect(None, username, password)
sftp = paramiko.SFTPClient.from_transport(transport)

# make dict with email + group
remote_file = list(sftp.open('www/tiredsosha.ru/passworkp.csv'))
remote_dict = {}
for word in remote_file:
    sword = str(word).strip().split(',')
    remote_dict[sword[0]] = sword[1]

# make dict for login and passcode for groups
dictionary = {}
with open('//home//hc//slackbot//keys.txt') as file:
    file = file.readlines()
    for lines in file:
        word = lines.split()
        dictionary[word[0]] = (word[1], word[2])

#connection with slack app
client = slack.WebClient(token=os.environ['slack_token'])
bot_id = client.api_call('auth.test')['user_id']

# '/help' event
@app.route('/slack/help', methods=['POST'])
def welcome_message():
    data = request.form
    user = data.get('user_id')
    if user != None and bot_id != user:
        client.chat_postMessage(channel=f'{user}', text='Для того, чтобы получить пароль от пассворка, напиши "/passwork"\nЕсли что-то не работает, напиши Саше Чичко :(')
    return Response(), 200

# '/passwork' event
@app.route('/slack/passwork', methods=['POST'])
def passwork_message():
    data = request.form
    user = data.get('user_id')
    if user != None and bot_id != user:
        client.chat_postMessage(channel=f'{user}', text='\nПожалуйста, напиши свою почту, и я на нее скину на нее доступ')
    return Response(), 200


# any massage event
@slack_event_handler.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    try: # take email from payload
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text).group()
    except AttributeError:
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    print(email)

    if email == None: # handle emails
        if user_id != None and bot_id != user_id:
            client.chat_postMessage(channel=f'{user_id}', text='Приветики, я супербот Hello!\nНапиши "/help", и я расскажу, что умею :)')
    else:
        dep_value = remote_dict.get(email, None)
        print(dep_value)
        if user_id != None and bot_id != user_id:
            if dep_value == None:
                client.chat_postMessage(channel=f'{user_id}', text="\nскорее всего ошибка в почте, можешь попробовать использовать алиас, если не помогло, напиши Саше Чичко")
            elif dep_value == 'tech':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'hr':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'developer':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'market':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'design':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'manager':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'buh':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'office':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'sapozh':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'dubarov':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'korch':
                passwork_responce(email, dep_value, user_id)
            elif dep_value == 'admin':
                passwork_responce(email, dep_value, user_id,'')
            elif dep_value == 'myho':
                client.chat_postMessage(channel=f'{user_id}', text="Дорогая, Полина Евгеньевна, проверьте свою почту")
                email_passcode(email, 'я вас очень люблю, но пароль вы не получите, досвидули\nбубубуб\nбипка')


        if user_id != None and bot_id != user_id:
            client.chat_postMessage(channel=f'{user_id}', text="\nскорее всего ошибка в почте, можешь попробовать использовать алиас, если не помогло, напиши Саше Чичко")

# start server only if script start directly
if __name__ == '__main__':
    app.run(host="10.0.22.215", port=5000, debug=True)
