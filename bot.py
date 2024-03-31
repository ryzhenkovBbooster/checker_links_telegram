import asyncio
import json
import os
import textwrap
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from dotenv import load_dotenv

from src.config.misc import redis
from src.filters.filter import UserAccessFilter
from src.handlers import file_crud, check_urls
from src.keyboards.check_and_crud_file_k import main_key, stop_key, pre_config_key
from src.service.crud_file_service import get_data_files
from workerTelegramCheck.loop_checker import loop_check_work

load_dotenv()
stop_check_event = asyncio.Event()
stop_send_event = asyncio.Event()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(storage=RedisStorage(redis=redis))

@dp.message(Command("start"), UserAccessFilter())
async def cmd_start(message: Message):
    # script_path = Path(__file__).resolve()
    # lib_path = os.path.join(script_path.parent, 'lib_files')
    # lib_path = Path(lib_path)
    # urls_path = get_data_files(lib_path / 'urls', 'urls.txt')
    # proxies_path = get_data_files(lib_path / 'proxy', 'proxy.txt')
    #
    # if urls_path == False or proxies_path == False:
    #     await message.answer('Добрый день', reply_markup=pre_config_key())
    await message.answer('Добрый день', reply_markup=main_key())

async def send_unactive_urls():
    while not stop_send_event.is_set():
        try:
            unactive_urls = await redis.get('unactive_cache')
            if unactive_urls:

                unactive_urls = json.loads(unactive_urls)

                for i in unactive_urls:
                    await asyncio.sleep(0.5)

                    if stop_send_event.is_set():
                        break
                    await bot.send_message(chat_id=os.getenv('USER_ID'), text=f'{i.replace("https://t.me/", "@")}')

        except Exception as e:
            print(e)



@dp.message(F.text.lower() == 'начать поиск 🔍', UserAccessFilter())
async def start_check_loop(message: Message):
    await redis.delete('unactive_cache')
    script_path = Path(__file__).resolve()
    lib_path = os.path.join(script_path.parent, 'lib_files')
    lib_path = Path(lib_path)
    urls_path = get_data_files(lib_path / 'urls', 'urls.txt')
    proxies_path = get_data_files(lib_path / 'proxy', 'proxy.txt')
    await message.answer('Перебор начался', reply_markup=stop_key())
    asyncio.create_task(loop_check_work(proxies=proxies_path, urls=urls_path, stop_check_event=stop_check_event))
    asyncio.create_task(send_unactive_urls())

@dp.message(F.text.lower() == 'стоп ⛔', UserAccessFilter())
async def stop_check_loop(message: Message):
    stop_send_event.set()
    stop_check_event.set()


    stop_send_event.clear()
    stop_check_event.clear()# Устанавливаем событие для остановки цикла проверки
    await message.reply("Операция завершена", reply_markup=main_key())
    await redis.delete('unactive_cache')

async def main():

    dp.include_routers(file_crud.router, check_urls.router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)



if __name__ == "__main__":
    # queue = asyncio.Queue()
    asyncio.run(main())