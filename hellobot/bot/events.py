import re
import requests
import slack

from random import randint
from bs4 import BeautifulSoup


class Events:
    def __init__(self, app, bot, userdata, mail, boys_wisdom, wolf_wisdom):
        self.app = app
        self.bot = bot
        self.mail = mail
        self.userdata = userdata
        self.boys_wisdom = boys_wisdom
        self.wolf_wisdom = wolf_wisdom
        self.client, self.bot_id = self.start()
        self.user = None
        self.helpers = [
            'помощ', 'проблем', 'хуйня', 'не работ', 'help', 'помог',
            'пассворк', 'passwork', '/help'
        ]
        self.humores = ['шутк', 'анек', 'смех', 'юмор']
        self.boy = ['пацан', 'брат', 'брат,']
        self.wolf = ['мудрость', 'волк', 'волч']

    def start(self):
        client = slack.WebClient(self.bot.token)
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
Я немного эволюционировал и умею только давать пароль от пассворка, рассказать анекдот, поделиться словом пацана или мудростью волка
Хочешь попасть в пассворк: отправь мне свою рабочую почту
Хочешь посмеяться: напиши "Хочу анекдот"
Хочешь узнать о жизни пацана: напиши "Брат, помоги"
А если хочешь помудреть: напиши "Поделись мудростью"'''
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

    def custom(self, key_dict: dict, irange: tuple):
        start, stop = irange
        self.replay(key_dict.get(randint(start, stop)))

    def passwork(self, email, username, password, master_pass):
        text = 'Кинул тебе пароль от пассворка на почту'
        self.replay(text)
        body = f'Лови логин и пароль для passwork\nЛогин: {username}\nПароль: {password}\nМастер-пароль: {master_pass}(вводить вторым)'
        self.mail.send(body=body, user=email)

    def error(self):
        text = 'Такой почты нет в моей базе, перепроверь ее написание, пожалуйста\nЕсли ошибка возникает не первый раз напиши Артему Паламарчуку'
        self.replay(text)

    def email_validator(self, data):
        try:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data).group()
        except AttributeError:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data)
        return email

    def email_true(self, email):
        for pair in self.userdata.items():
            if email in pair[1].users:
                key = pair[0]
                break
            else:
                key = None
        def get_creds(what: str):
            cred = self.userdata[key].credentials[what]
            return cred
        if key:
            username = get_creds('username')
            password = get_creds('password')
            master_pass = get_creds('master')
            self.passwork(email, username, password, master_pass)
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
        for key in self.boy:
            if key in text:
                irange = (1, 100)
                self.custom(self.boys_wisdom, irange)
                word = True
                break
        for key in self.wolf:
            if key in text:
                irange = (1, 43)
                self.custom(self.wolf_wisdom, irange)
                word = True
                break
        if not word:
            self.hello()
