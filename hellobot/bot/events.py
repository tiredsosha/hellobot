import asyncio
import slack
import re
import aiohttp

from bs4 import BeautifulSoup


class Events:
    def __init__(self, app, instance):
        self.app = app
        self.instance = instance
        self.client, self.bot_id = self.start()
        self.user = None

    def start(self):
        client = slack.WebClient(self.instance.token)
        bot_id = client.api_call('auth.test')['user_id']

        return client, bot_id

    async def replay(self, text):
        if self.user != None and self.bot_id != self.user:
            self.client.chat_postMessage(channel=f'{self.user}', text=text)

    def message(self, payload):
        event = payload.get('event', {})
        self.user = event.get('user')
        text = event.get('text')

    async def help(self):
        text = 'Напиши мне свою рабочую почту (не алиас).\nНапример s.rek@hello.io\nНу, а если хочешь анекдот, то так и напиши'
        task = asyncio.create_task(self.replay(text))

    async def hello(self):
        text = '''Привет, я Hello бот!
        Пока я умею только давать пароль от пассворка и могу рассказать анекдот
        Отправь мне свою рабочую почту или напиши "Хочу анекдот"'''
        task = asyncio.create_task(self.replay(text))

    async def humor(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://baneks.ru/random') as resp:
                try:
                    soup = BeautifulSoup(await resp.text(), 'html.parser')
                    text = soup.find("p").text
                except UnicodeDecodeError:
                    text = 'Китайские дети утром делают зарядку, а вечером относят её в "Евросеть"'

                task = asyncio.create_task(self.replay(text))

    async def passwork(self):
        text = 'Кинул тебе пароль от пассворка на почту'
        task = asyncio.create_task(self.replay(text))

    async def error(self):
        text = 'Такой почты нет в моей базе, перепроверь ее написание, пожалуйста\nЕсли ошибка возникает не первый раз напиши Артему Паламарчуку'

    async def email_validator(data):
        try:  # take email from payload
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data).group()
        except AttributeError:
            email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', data)
