from aiogram.filters import BaseFilter
from aiogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()

class UserAccessFilter(BaseFilter):
    async def __call__(self, message: Message):
        if message.from_user.id == int(os.getenv('USER_ID')):
            return True

        await message.answer('Нет доступа')
        return False