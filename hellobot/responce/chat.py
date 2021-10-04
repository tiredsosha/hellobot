from aiohttp import web


class Requests:
    def __init__(self, bot_id, client):
        self.bot_id = bot_id
        self.client = client

    async def replay(self, user, text):
        if user != None and self.bot_id != user:
            self.client.chat_postMessage(channel=f'{user}', text=text)

    @staticmethod
    async def help(request):
        user = request.form.get('user_id')
        Replays.replay
        return web.Response(status=200)

    @staticmethod
    async def passwork(request):
        print(request)
        return web.Response(status=200)


class Replays:
    

    
