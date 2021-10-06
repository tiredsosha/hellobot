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

with open('configs/user.yaml') as users:
    users = Users(**yaml.safe_load(users))

with open('configs/email.yaml') as email:
    email = Email(**yaml.safe_load(email))

with open('configs/credentials.yaml') as creds:
    creds = from_dict(yaml.safe_load(creds))


def connect_bot(app, msg, server, creds):
    task = []
    bot = Bot
    event_handler = SlackEventAdapter(bot.singing, bot.endpoint, app)

    loop = asyncio.get_event_loop()
    event = Events(app, creds, bot, msg, server)

    @event_handler.on('message')
    def messages(payload):
        task.append(loop.create_task(event.message(payload)))


def main(data, creds):
    # app = web.Application()
    # app.add_routes(web.post('/slack', for_lool))
    # app = web.Application()
    app = Flask(__name__)

    @app.route('/slack')
    def for_lool(request):
        return "ты чмырь"

    mail = Send(data.username, data.password, data.smtp_server, data.smtp_port)
    e_server = mail.start()
    e_msg = mail.message()

    connect_bot(app, e_msg, e_server, creds)
    app.run(host="10.0.22.215", port=5000, debug=True)
    # web.run_app(app, host='10.0.22.215', port=5000)


if __name__ == "__main__":
    main(email, creds)