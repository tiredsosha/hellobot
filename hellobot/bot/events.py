import asyncio
import slack
import re
import aiohttp

from bs4 import BeautifulSoup

from hellobot.mail.email import Send


class Events:
    def __init__(self, app, creds, instance, msg, server):
        self.app = app
        self.instance = instance
        self.creds = creds
        self.msg = msg
        self.server = server
        self.client, self.bot_id = self.start()
        self.user = None
        self.helpers = ['помощ', 'проблем', 'хуйня', 'не работ', 'help']
        self.humores = ['шутк', 'анек', 'смех', 'юмор']
        self.helloes = [
            'прив', 'парол', 'пассворк', 'хранилище', 'доступ', 'passwork'
        ]

    def start(self):
        client = slack.WebClient(self.instance.token)
        bot_id = client.api_call('auth.test')['user_id']
        print('bot started')

        return client, bot_id

    def replay(self, text):
        print('replay stage')
        if self.user != None and self.bot_id != self.user:
            self.client.chat_postMessage(channel=f'{self.user}', text=text)

    def email_validator(self, data):
        try:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data).group()
        except AttributeError:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data)
        print(email)
        return email

    def email_true(self, text):
        for pair in self.instance:
            if text in pair[1]:
                key = pair[0]
                break
            else:
                key = None
        print(key)

        if key:
            username = self.creds[key].username
            password = self.creds[key].password
            self.passwork()
            body = f'Лови логин и пароль для passwork\nЛогин: {username}\nПароль: {password}'
            self.replay(text)
            Send.send(self.msg, self.server, body=body, user=text)
        else:
            self.error()

    def email_false(self, text):
        for key in self.helpers:
            if key in text:
                self.help()
                break
        for key in self.humores:
            if key in text:
                asyncio.run(self.humor())
                break
        for key in self.helloes:
            if key in text:
                self.hello()
                break

    def message(self, payload):
        print(payload)
        event = payload.get('event', {})
        self.user = event.get('user')
        text = event.get('text').lower()
        email = self.email_validator(text)
        if email: self.email_true(email)
        else: self.email_false(text)

    def help(self):
        print('help stage')
        text = 'Напиши мне свою рабочую почту (не алиас).\nНапример s.rek@hello.io\nНу, а если хочешь анекдот, то так и напиши'
        self.replay(text)

    def hello(self):
        print('hello stage')
        text = '''Привет, я Hello бот!
Пока я умею только давать пароль от пассворка и могу рассказать анекдот
Отправь мне свою рабочую почту или напиши "Хочу анекдот"'''
        self.replay(text)

    async def humor(self):
        print('humor stage')
        with aiohttp.ClientSession() as session:
            with session.get('https://baneks.ru/random') as resp:
                try:
                    soup = BeautifulSoup(resp.text(), 'html.parser')
                    text = soup.find("p").text
                except UnicodeDecodeError:
                    text = 'Китайские дети утром делают зарядку, а вечером относят её в "Евросеть"'

                self.replay(text)

    def passwork(self):
        print('passwork stage')
        text = 'Кинул тебе пароль от пассворка на почту'
        self.replay(text)

    def error(self):
        print('error stage')
        text = 'Такой почты нет в моей базе, перепроверь ее написание, пожалуйста\nЕсли ошибка возникает не первый раз напиши Артему Паламарчуку'
        self.replay(text)
