import asyncio
import json
from itertools import cycle
import random

from responseToLinkAccount.checkTelegramLink import fetch
from src.config.misc import redis


# proxies = [
#     "217.29.63.159:13580:k5jmRs:1oXovq",
#     "217.29.63.159:13579:k5jmRs:1oXovq",
#     "217.29.63.240:12233:k5jmRs:1oXovq",
#     "217.29.63.240:12232:k5jmRs:1oXovq",
#     "217.29.63.240:12231:k5jmRs:1oXovq",
#     "217.29.63.202:13541:k5jmRs:1oXovq",
# ]
# urls = [
#     "https://t.me/ArcaneAngel",
#     "https://t.me/ArcticPhoenix",
#     "https://t.me/AstralMage",
#     "https://t.me/ArcticWolf",
#     "https://t.me/AstralAurora",
#     "https://t.me/AtomicThunder",
#     "https://t.me/AuroraBorealis",
#     "https://t.me/BladeMaster",
#     "https://t.me/BlazePhoenix",
#     "https://t.me/BlazeStorm",
#     "https://t.me/BlazeDancer",
#     "https://t.me/BloodOath",
#     "https://t.me/CelestialChampion",
#     "https://t.me/BloodmoonHunter",
#     "https://t.me/CelestialFire",
#     "https://t.me/BlazeTheDragon",
#     "https://t.me/CrimsonCobra",
#     "https://t.me/CosmicKnight",
#     "https://t.me/CrypticGamer",
#     "https://t.me/DarkAngel",
#     "https://t.me/DoomBringer",
#     "https://t.me/DragonFury",
#     "https://t.me/EternalFury",
#     "https://t.me/EternalVanguard",
#     "https://t.me/EtherealBlade",
#     "https://t.me/EternalWarlords",
#     "https://t.me/EtherealEclipse",
#     "https://t.me/EtherealEmissary",
#     "https://t.me/EtherealEmpress",
#     "https://t.me/FireDragon",
#     "https://t.me/AmethystArrow",
#     "https://t.me/FlameStorm",
#     "https://t.me/AncientArcher",
#     "https://t.me/FrostFalcon",
#     "https://t.me/FrostFox",
#     "https://t.me/FrostFire",
#     "https://t.me/AndroidAce",
#     "https://t.me/FrostRaven",
#     "https://t.me/ArcaneSoul",
#     "https://t.me/FrozenFlame",
#     "https://t.me/AzureAce",
#     "https://t.me/BladeDancer",
#     "https://t.me/GalacticAdventurer",
#     "https://t.me/FuriousFalcon",
#     "https://t.me/GhostGladiator",
#     "https://t.me/BlazeFury",
#     "https://t.me/GhostStriker",
#     "https://t.me/GoldenGuardian",
#     "https://t.me/GoldenSnitch",
#     "https://t.me/GrayGhost",
#     "https://t.me/GrimGhost",
#     "https://t.me/GrimReaper",
#     "https://t.me/IceBlast",
#     "https://t.me/IceInferno",
#     "https://t.me/FrostGhost",
#     "https://t.me/IceNinja",
# ]

async def loop_check(urls, proxies):
    unactive = []
    tasks = []
    random.shuffle(proxies)
    print(proxies)
    proxy_cycle = cycle(proxies)  # Итератор для равномерного распределения прокси

    for url in urls:
        proxy = next(proxy_cycle)  # Получаем следующий прокси из списка
        task = asyncio.create_task(fetch(url, proxy))
        tasks.append(task)

    data = await asyncio.gather(*tasks)
    for i in data:
        if i[0] in proxies:
            proxies.remove(i[0])
        if i[0] == 'false':
            unactive.append(i[1])

    return proxies, unactive


def work_loop(urls, proxies):

    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_check(urls, proxies))

async def loop_check_work( urls: str, proxies: str, stop_check_event):
    while not stop_check_event.is_set():
        # print(proxies)

        if len(proxies) == 0:
            break
        # loop = asyncio.get_event_loop()
        # err_data, proxies = loop.run_until_complete(loop_check(urls, proxies))
        proxies, unactive = await loop_check(urls, proxies)
        if unactive != 0:

            unactive = json.dumps(unactive)
            cache_unactive = await redis.get('unactive_cache')
            if cache_unactive is not None:
                cache_unactive = json.loads(cache_unactive)


            if cache_unactive != json.loads(unactive):
                proxies, unactive = await loop_check(json.loads(unactive), proxies)
                if unactive != 0:
                    unactive = json.dumps(unactive)


                    await redis.set('unactive_cache', unactive, ex=86400)




        await asyncio.sleep(300)



          # Обновляем список URL для повторной проверки
# if __name__ == "__main__":
#     ''
