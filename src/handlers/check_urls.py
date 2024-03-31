import os
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message
from dotenv import load_dotenv

from src.filters.filter import UserAccessFilter
from src.service.check_proxy import check_proxies
from src.service.crud_file_service import get_data_files

router = Router()
load_dotenv()

# @router.message(F.text.lower() == 'start check')
# async def start_check(message: Message):
#     await message.answer('Проверка началась')

@router.message(F.text.lower() == 'check proxy', UserAccessFilter())
async def check_proxy(message: Message):
    await message.answer('проверка началась')
    script_path = Path(__file__).resolve()
    lib_path = os.path.join(script_path.parent.parent.parent, 'lib_files')
    lib_path = Path(lib_path)

    proxies_path = get_data_files(lib_path / 'proxy', 'proxy.txt')
    await check_proxies(proxies_path)

# async def send_unactive_urls(message: Message, unactive_urls: list[str]):
#     await message.bot.send_message(os.getenv('USER'), f'{unactive_urls}')
