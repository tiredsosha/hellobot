import os
import re
import email_func as efunc
import slack
import paramiko
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, request
from slackeventsapi import SlackEventAdapter


# Open a transport
host, port = "p592058.ftp.ihc.ru", 22
transport = paramiko.Transport((host, port))
username, password = "p592058", "Minks!2012"
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


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# make server that lisens to slack events
app = Flask(__name__)
slack_event_handler = SlackEventAdapter(os.environ['slack_singing'], '/slack/events', app)


#connection with slack app
client = slack.WebClient(token=os.environ['slack_token'])
bot_id = client.api_call('auth.test')['user_id']


def email_responce(email, key, user_id, master=os.environ['master_pass']):

    client.chat_postMessage(channel=f'{user_id}', text="\nжди письмеца c парольчиком на почте\nпока-пока")
    efunc(email, f'login: {dictionary.get(key, None)[0]}\npassword: {dictionary.get(key, None)[1]}\nмастер пароль: {master}\n\n\n\n\n\n\nShRaK')
    efunc.send_email()


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

    try:
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text).group()
    except AttributeError:
        email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)

    if email == None:
        if user_id != None and bot_id != user_id:
            client.chat_postMessage(channel=f'{user_id}', text='Приветики, я супербот Hello!\nНапиши "/help", и я расскажу, что умею :)')
    else:
        try:
            if user_id != None and bot_id != user_id:
                dep_value = remote_dict.get(email, None)

                if dep_value == None:
                    client.chat_postMessage(channel=f'{user_id}', text="\nскорее всего ошибка в почте, можешь попробовать использовать алиас, если не помогло, напиши Саше Чичко")
                elif dep_value == 'admin':
                    email_responce(email, dep_value, user_id,'Sayid20sir20ah!')
                elif dep_value == 'myho':
                    client.chat_postMessage(channel=f'{user_id}', text="Дорогая, Полина Евгеньевна, проверьте свою почту")
                    email_responce(email, 'я вас очень люблю, но пароль вы не получите, досвидули\nбубубуб\nбипка')
                else:
                    email_responce(email, dep_value, user_id)

        except Exception:
            if user_id != None and bot_id != user_id:
                client.chat_postMessage(channel=f'{user_id}', text="\nскорее всего ошибка в почте, можешь попробовать использовать алиас, если не помогло, напиши Саше Чичко")


if __name__ == '__main__':
    app.run(host="10.0.22.175", port=5000, debug=True)
