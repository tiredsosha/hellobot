import aiohttp
import asyncio
from bs4 import BeautifulSoup

url = 'https://baneks.ru/random'


async def main(urk):
    async with aiohttp.ClientSession() as session:
        async with session.get(urk) as resp:
            try:
                soup = BeautifulSoup(await resp.text(), 'html.parser')
                humor = soup.find("p").text
            except UnicodeDecodeError:
                humor = 'Китайские дети утром делают зарядку, а вечером относят её в "Евросеть"'

            print(humor)


loop = asyncio.get_event_loop()

loop.run_until_complete(main(url))