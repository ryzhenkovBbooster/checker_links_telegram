from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Начать поиск 🔍')
    kb.button(text='Настройка ⚙️')
    # kb.button(text='Загрузка proxy 🔐')

    return kb.as_markup(resize_keyboard=True)


def stop_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Стоп ⛔')


    return kb.as_markup(resize_keyboard=True)

def cancel_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Отмена 🚫')


    return kb.as_markup(resize_keyboard=True)

def pre_config_key():

    # kb = ReplyKeyboardBuilder()

    # kb.button(text='Загрузка базы 📚')
    # kb.button(text='Загрузка proxy 🔐')
    # kb.button(text='Назад')
    #
    # return kb.as_markup(resize_keyboard=True)
    kb = [
        [types.KeyboardButton(text="Загрузка базы 📚")],
        [types.KeyboardButton(text="Загрузка proxy 🔐")],
        [types.KeyboardButton(text="Назад")]

    ]
    # keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # keyboard.add(KeyboardButton('Загрузка базы 📚'))
    # keyboard.add(KeyboardButton('Загрузка proxy 🔐'))
    # keyboard.add(KeyboardButton('Назад'))
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard