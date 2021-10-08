import asyncio
from slackeventsapi import SlackEventAdapter
import yaml

from flask import Flask

from hellobot.bot.events import Events
from hellobot.entities.email import Email
from hellobot.entities.user import Users
from hellobot.entities.bot import Bot
from hellobot.mail.email import Send
from hellobot.entities.cred import from_dict


def connect_bot(app, creds, users, mail):
    tasks = []
    bot = Bot()
    event_handler = SlackEventAdapter(bot.singing, bot.endpoint, app)
    event = Events(app, creds, bot, users, mail)

    @event_handler.on('message')
    def messages(payload):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            tasks.append(loop.create_task(event.message(payload)))
        else:
            asyncio.run(event.message(payload))


def main():
    with open('configs/users.yaml') as users:
        users = Users(**yaml.safe_load(users))
    with open('configs/email.yaml') as email:
        email = Email(**yaml.safe_load(email))
    with open('configs/credentials.yaml') as creds:
        creds = from_dict(yaml.safe_load(creds))

    app = Flask(__name__)

    @app.route('/slack')
    def for_lool(request):
        return "ты чмырь"

    mail = Send(email.username, email.password, email.smtp_server,
                email.smtp_port)

    connect_bot(app, creds, users, mail)
    app.run(host="10.0.22.215", port=5000, debug=False)


main()