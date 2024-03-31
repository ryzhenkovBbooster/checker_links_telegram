import asyncio

from aiogram.client.session import aiohttp

def format_proxy(proxy):
    ip, port, username, password = proxy.split(':')
    return f'http://{username}:{password}@{ip}:{port}'
async def check_proxy(session, proxy):
    proxy_url = format_proxy(proxy)

    try:
        async with session.get('https://t.me/example', proxy=proxy_url, timeout=5) as response:
            if response.status == 200:
                print(f'Работает: {proxy}')
                return proxy
            else:
                print(f'Не работает: {proxy}')
    except Exception as e:
        print(f'Ошибка: {proxy}, {e}')
    return None

async def check_proxies(proxy_list):
    async with aiohttp.ClientSession() as session:
        tasks = [check_proxy(session, proxy) for proxy in proxy_list]
        working_proxies = await asyncio.gather(*tasks)
        return [proxy for proxy in working_proxies if proxy]