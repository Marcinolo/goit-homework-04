import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta


async def get_page(url, session):
    async with session.get(url, ssl=False) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        return f"Body: {html[:15]}..."


async def get_exchange_rates(session, date):
    url = f"https://api.nbp.pl/api/exchangerates/tables/a/{date}?format=json"
    return await get_page(url, session)


async def main():
    current_date = datetime.now().strftime("%Y-%m-%d")
    async with aiohttp.ClientSession() as session:
        tasks = [get_exchange_rates(session, (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")) for i in
                 range(10)]
        result = await asyncio.gather(*tasks)
        return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    result = asyncio.run(main())
    print(result)
