import asyncio
from email import message
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
        self.tasks = []
        self.helpers = ['помощ', 'проблем', 'хуйня', 'не работ', 'help']
        self.humores = ['шутк', 'анек', 'смех', 'юмор']
        self.helloes = [
            'прив', 'парол', 'пассворк', 'хранилище', 'доступ', 'passwork'
        ]

    def start(self):
        client = slack.WebClient(self.instance.token)
        bot_id = client.api_call('auth.test')['user_id']

        return client, bot_id

    async def replay(self, text):
        if self.user != None and self.bot_id != self.user:
            self.client.chat_postMessage(channel=f'{self.user}', text=text)

    async def email_validator(data):
        try:  # take email from payload
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data).group()
        except AttributeError:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data)
        return email

    async def email_true(self, text):
        if text in self.emails:
            await self.passwork()
            body = f'Лови логин и пароль для passwork\n{user_pass}'
            self.tasks.append(asyncio.create_task(self.replay(text)))
            self.tasks.append(asyncio.create_task(Send.send(self.msg, self.server, body=, user=)))
        else:
            await self.error()

    async def email_false(self, text):
        for key in self.helpers:
            if key in text:
                await self.help()
                break
        for key in self.humores:
            if key in text:
                await self.humor()
                break
        for key in self.helloes:
            if key in text:
                await self.hello()
                break

    async def message(self, payload):
        event = payload.get('event', {})
        self.user = event.get('user')
        text = event.get('text').lower()
        email = await self.email_validator(text)
        if email: await self.email_true(email)
        else: await self.email_false(text)

    def help(self):
        text = 'Напиши мне свою рабочую почту (не алиас).\nНапример s.rek@hello.io\nНу, а если хочешь анекдот, то так и напиши'
        self.tasks.append(asyncio.create_task(self.replay(text)))

    async def hello(self):
        text = '''Привет, я Hello бот!
        Пока я умею только давать пароль от пассворка и могу рассказать анекдот
        Отправь мне свою рабочую почту или напиши "Хочу анекдот"'''
        self.tasks.append(asyncio.create_task(self.replay(text)))

    async def humor(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://baneks.ru/random') as resp:
                try:
                    soup = BeautifulSoup(await resp.text(), 'html.parser')
                    text = soup.find("p").text
                except UnicodeDecodeError:
                    text = 'Китайские дети утром делают зарядку, а вечером относят её в "Евросеть"'

                self.tasks.append(asyncio.create_task(self.replay(text)))

    async def passwork(self):
        text = 'Кинул тебе пароль от пассворка на почту'
        self.tasks.append(asyncio.create_task(self.replay(text)))

    async def error(self):
        text = 'Такой почты нет в моей базе, перепроверь ее написание, пожалуйста\nЕсли ошибка возникает не первый раз напиши Артему Паламарчуку'
        self.tasks.append(asyncio.create_task(self.replay(text)))
