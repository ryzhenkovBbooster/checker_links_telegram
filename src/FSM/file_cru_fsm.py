from aiogram.fsm.state import StatesGroup, State


class CrudFiles(StatesGroup):
    get_file_proxies = State()
    get_file_urls = State()
