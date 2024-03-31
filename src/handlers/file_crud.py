import os
from pathlib import Path

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.FSM.file_cru_fsm import CrudFiles
from src.filters.filter import UserAccessFilter
from src.keyboards.check_and_crud_file_k import main_key, cancel_key, pre_config_key
from src.service.crud_file_service import create_dir_if_not_exists, get_data_files

router = Router()


@router.message(F.text.lower() == 'загрузка proxy 🔐', UserAccessFilter())
async def get_file_proxy(message: Message, state: FSMContext):
    await message.answer('Отправьте файл с расширением .txt', reply_markup=cancel_key())
    await state.set_state(CrudFiles.get_file_proxies)


@router.message(F.document, CrudFiles.get_file_proxies)
async def upload_file_proxy(message: Message, state: FSMContext):
    document_id = message.document.file_id
    file = await message.bot.get_file(document_id)
    script_path = Path(__file__).resolve()
    file_path = file.file_path

    lib_path = os.path.join(script_path.parent.parent.parent, 'lib_files', 'proxy')

    dir_path = create_dir_if_not_exists(lib_path)
    proxy_list = Path(dir_path)

    dir_path = f'{dir_path}/proxy.txt'

    await message.bot.download_file(file_path, dir_path)
    proxy_list = (get_data_files(proxy_list, 'proxy.txt'))


    await message.answer('Готов к работе')
    await message.answer(f'Загружено {len(proxy_list)} proxy', reply_markup=main_key() )
    await state.clear()

@router.message(F.text.lower() == 'загрузка базы 📚', UserAccessFilter())
async def get_file_urls(message: Message, state: FSMContext):
    await message.answer('Отправьте файл с расширением .txt', reply_markup=cancel_key())
    await state.set_state(CrudFiles.get_file_urls)


@router.message(F.document, CrudFiles.get_file_urls)
async def upload_file_urls(message: Message, state: FSMContext):
    document_id = message.document.file_id
    file = await message.bot.get_file(document_id)
    script_path = Path(__file__).resolve()
    file_path = file.file_path

    lib_path = os.path.join(script_path.parent.parent.parent, 'lib_files', 'urls')

    dir_path = create_dir_if_not_exists(lib_path)
    urls_list = Path(dir_path)


    dir_path = f'{dir_path}/urls.txt'
    await message.bot.download_file(file_path, dir_path)
    urls_list = get_data_files(urls_list, 'urls.txt')

    await message.answer('Готов к работе')

    await message.answer(f'Загружено {len(urls_list)} ссылок', reply_markup=main_key())
    await state.clear()

@router.message(F.text.lower() == 'настройка ⚙️', UserAccessFilter())
async def config_data(message: Message):
    await message.answer('Добавьте в бота прокси и аккаунты для начала работы', reply_markup=pre_config_key())
@router.message(F.text.lower() == 'отмена 🚫', UserAccessFilter(), CrudFiles.get_file_urls)
@router.message(F.text.lower() == 'отмена 🚫', UserAccessFilter(), CrudFiles.get_file_proxies)
async def cancel_update_data(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Операция отменена', reply_markup=pre_config_key())

@router.message(F.text.lower() == 'назад', UserAccessFilter())
async def back_to_menu(message: Message):
    await message.answer('Главное меню', reply_markup=main_key())
