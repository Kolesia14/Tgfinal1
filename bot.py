import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import asyncio
import csv
import os

API_TOKEN = '7936347209:AAH8eoTv4ifiluLPa_uUE4xK2YqC8TPOtvo'
admins = [356538599]  # Ваши Telegram ID

# Включаем логирование, чтобы не пропустить ошибки
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Команды и функции для бота

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Я бот для учёта листового металла.\nИспользуйте меню для работы с материалами.")

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.reply("Используйте команды для работы с материалами:\n- /view_materials для просмотра материалов\n- /add_material для добавления материала (только для администраторов)\n- /edit_material для редактирования материала (только для администраторов)\n- /delete_material для удаления материала (только для администраторов)")

# Команды для работы с материалами
@dp.message_handler(commands=['view_materials'])
async def view_materials(message: types.Message):
    # Отображение всех материалов
    with open('materials.csv', mode='r') as file:
        reader = csv.reader(file)
        materials = "\n".join([f"{row[0]} - {row[1]} - {row[2]} шт" for row in reader])
    await message.reply(f"Список материалов:\n{materials}")

@dp.message_handler(commands=['add_material'])
async def add_material(message: types.Message):
    # Добавление материала (только для администраторов)
    if message.from_user.id not in admins:
        await message.reply("У вас нет прав для добавления материалов.")
        return

    # Получение данных от пользователя
    await message.reply("Введите данные материала в формате:\nНазвание (толщина x размер) - количество (например, '4мм(1250×2500мм) - 10шт')")
    await message.answer("Введите данные:")

@dp.message_handler(commands=['edit_material'])
async def edit_material(message: types.Message):
    # Редактирование материала (только для администраторов)
    if message.from_user.id not in admins:
        await message.reply("У вас нет прав для редактирования материалов.")
        return

    # Получение данных от пользователя
    await message.reply("Введите новые данные для материала в формате:\nНазвание (толщина x размер) - количество")
    await message.answer("Введите данные:")

@dp.message_handler(commands=['delete_material'])
async def delete_material(message: types.Message):
    # Удаление материала (только для администраторов)
    if message.from_user.id not in admins:
        await message.reply("У вас нет прав для удаления материалов.")
        return

    # Получение данных от пользователя
    await message.reply("Введите название материала, который нужно удалить:")
    await message.answer("Введите данные:")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)