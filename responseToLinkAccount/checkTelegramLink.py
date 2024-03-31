import asyncio
from urllib.parse import urlparse
import random
import aiohttp
import aiohttp_socks
import requests
from aiohttp import ClientProxyConnectionError, ClientHttpProxyError, ClientConnectorError
from aiohttp_socks import ProxyConnector
from fake_useragent import UserAgent
ua = UserAgent(platforms='pc', os=['windows', 'macos'], browsers=["chrome", "edge", "firefox",])
async def fetch(url, proxy):

    ip, port, username, password = proxy.split(":")
    # parsed_proxy = urlparse(f"http://{proxy}")
    connector = ProxyConnector(
        proxy_type=aiohttp_socks.ProxyType.HTTP,
        host=ip,
        port=int(port),
        username=username,
        password=password,



    )
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        try:
            async with session.get(url, ssl=False) as response:
                response_text = await response.text()
                if 'tgme_page_title' in response_text:
                    return ('True', url)
                else:
                    return ('false', url)


                # Здесь можно добавить обработку ответа
        except (ClientProxyConnectionError, ClientHttpProxyError, ClientConnectorError) as e:
            print(e)
            return (proxy, url)
        except asyncio.TimeoutError as e:
            print(e)
            return (proxy, url)
        except Exception as e:
            print(e)
            return (proxy, url)
        finally:
            await session.close()





