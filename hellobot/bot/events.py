import slack
import re
import requests

from bs4 import BeautifulSoup


class Events:
    def __init__(self, app, creds, instance, users_data, mail):
        self.app = app
        self.instance = instance
        self.creds = creds
        self.mail = mail
        self.users_data = users_data
        self.client, self.bot_id = self.start()
        self.user = None
        self.helpers = [
            'помощ', 'проблем', 'хуйня', 'не работ', 'help', 'помог'
        ]
        self.humores = ['шутк', 'анек', 'смех', 'юмор']
        self.helloes = [
            'прив', 'парол', 'пассворк', 'хранилище', 'доступ', 'passwork'
        ]

    def start(self):
        client = slack.WebClient(self.instance.token)
        bot_id = client.api_call('auth.test')['user_id']
        return client, bot_id

    def replay(self, text):
        print(self.user, self.bot_id, 'ID')
        if self.user != None and self.bot_id != self.user:
            self.client.chat_postMessage(channel=f'{self.user}', text=text)

    async def message(self, payload):
        event = payload.get('event', {})
        self.user = event.get('user')
        text = event.get('text').lower()
        email = self.email_validator(text)
        if email: self.email_true(email)
        else: self.email_false(text)

    def help(self):
        text = 'Напиши мне свою рабочую почту (не алиас).\nНапример s.rek@hello.io\nНу, а если хочешь анекдот, то так и напиши'
        self.replay(text)

    def hello(self):
        text = '''Привет, я Hello бот!
Пока я умею только давать пароль от пассворка и могу рассказать анекдот
Отправь мне свою рабочую почту или напиши "Хочу анекдот"'''
        self.replay(text)

    def humor(self):
        humor = requests.get('https://baneks.ru/random', timeout=10)
        humor = humor.text
        try:
            soup = BeautifulSoup(humor, 'html.parser')
            text = soup.find("p").text
        except UnicodeDecodeError:
            text = 'Китайские дети утром делают зарядку, а вечером относят её в "Евросеть"'
        self.replay(text)

    def passwork(self, username, password):
        text = 'Кинул тебе пароль от пассворка на почту'
        self.replay(text)
        body = f'Лови логин и пароль для passwork\nЛогин: {username}\nПароль: {password}'
        self.mail.send(body=body, user=text)

    def error(self):
        text = 'Такой почты нет в моей базе, перепроверь ее написание, пожалуйста\nЕсли ошибка возникает не первый раз напиши Артему Паламарчуку'
        self.replay(text)

    def email_validator(self, data):
        try:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data).group()
        except AttributeError:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data)
        return email

    def email_true(self, text):
        for pair in self.users_data:
            print(pair)
            if text in pair[1]:
                key = pair[0]
                break
            else:
                key = None
        if key:
            username = self.creds[key].username
            password = self.creds[key].password
            self.passwork(username, password)
        else:
            self.error()

    def email_false(self, text):
        word = False
        for key in self.helpers:
            if key in text:
                self.help()
                word = True
                break
        for key in self.humores:
            if key in text:
                self.humor()
                word = True
                break
        for key in self.helloes:
            if key in text:
                self.hello()
                word = True
                break
        if not word:
            self.hello()
