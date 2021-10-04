from aiohttp.web_routedef import post
import yaml

from aiohttp import web

from hellobot.bot.events import start_bot
from hellobot.responce.chat import Requests
from hellobot.entities.email import Email
from hellobot.entities.user import Users
from hellobot.entities.bot import Bot
from hellobot.responce.email import Send

with open('configs/user.yaml') as users:
    users = Users(**yaml.safe_load(users))

with open('configs/email.yaml') as email:
    email = Email(**yaml.safe_load(email))


def main(data):
    app = web.Application()
    app.add_routes([
        web.post('/slack/help', Requests.help),
        web.post('/slack/passwork', Requests.passwork)
    ])
    app = web.Application()
    web.run_app(app, host='10.0.22.215', port=5000)

    bot = Bot
    bot_id = start_bot(app, bot)

    mail = Send(data.username, data.password, data.smtp_server, data.smtp_port)
    e_server = mail.start()
    e_msg = mail.message()


if __name__ == "__main__":
    main()