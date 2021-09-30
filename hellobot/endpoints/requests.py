from aiohttp import web


class Requests:
    routes = web.RouteTableDef()

    @routes.post('/slack/help')
    async def help(request):
        data = request.form
        user = data.get('user_id')
        if user != None and bot_id != user:
            client.chat_postMessage(
                channel=f'{user}',
                text=
                'Для того, чтобы получить пароль от пассворка, напиши "/passwork"\nЕсли что-то не работает, напиши Саше Чичко :('
            )
        return web.Response(status=200)

    @routes.post('/slack/passwork')
    async def passwork(request):
        print(request)
        return web.Response(status=200)
