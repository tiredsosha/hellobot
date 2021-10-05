from slackeventsapi import SlackEventAdapter
import yaml

from aiohttp import web

from hellobot.bot.events import Events
from hellobot.responce.chat import Requests
from hellobot.entities.email import Email
from hellobot.entities.user import Users
from hellobot.entities.bot import Bot
from hellobot.responce.email import Send

with open('configs/user.yaml') as users:
    users = Users(**yaml.safe_load(users))

with open('configs/email.yaml') as email:
    email = Email(**yaml.safe_load(email))


def connect_bot(app):
    bot = Bot
    event_handler = SlackEventAdapter(bot.singing, bot.endpoint, app)
    event = Events(app, bot)
    return event


def main(data):
    app = web.Application()
    app.add_routes([
        web.post('/slack/help', Requests.help),
        web.post('/slack/passwork', Requests.passwork)
    ])
    app = web.Application()
    web.run_app(app, host='10.0.22.215', port=5000)

    mail = Send(data.username, data.password, data.smtp_server, data.smtp_port)
    e_server = mail.start()
    e_msg = mail.message()


if __name__ == "__main__":
    main()