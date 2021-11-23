import yaml
import asyncio

from slackeventsapi import SlackEventAdapter
from flask import Flask

from hellobot.bot.events import Events
from hellobot.entities.email import Email
from hellobot.entities.bot import Bot
from hellobot.entities.userdata import from_dict
from hellobot.mail.email import Send


def connect_bot(app, userdata, mail, boys, wolf):
    tasks = []
    bot = Bot()
    event_handler = SlackEventAdapter(bot.singing, bot.endpoint, app)
    event = Events(app, bot, userdata, mail, boys, wolf)

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
    with open('configs/email.yaml') as email:
        email = Email(**yaml.safe_load(email))
    with open('configs/userdata.yaml') as userdata:
        userdata = from_dict(yaml.safe_load(userdata))
    with open('configs/boys.yaml') as boys:
        boys = yaml.safe_load(boys)
    with open('configs/wolf.yaml') as wolf:
        wolf = yaml.safe_load(wolf)

    app = Flask(__name__)

    @app.route('/slack')
    def for_lool(request):
        return "ты чмырь"

    mail = Send(email.username, email.password, email.smtp_server,
                email.smtp_port)

    connect_bot(app, userdata, mail, boys, wolf)
    app.run(host="10.0.22.215", port=5000, debug=False)


main()