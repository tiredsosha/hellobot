import yaml

from aiohttp import web

from hellobot.bot.events import start_bot
from hellobot.endpoints.requests import Requests
from hellobot.entities.user import Users
from hellobot.entities.bot import Bot

with open('configs/user.yaml') as users:
    users = Users(**yaml.safe_load(users))


def main():
    app = web.Application()
    app.add_routes(Requests.routes)
    bot = Bot
    start_bot(app, bot)
    app = web.Application()
    app.add_routes(Requests.routes)
    web.run_app(app, host='10.0.22.215', port=5000)


if __name__ == "__main__":
    main()