from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config

bot = Bot(config.TELEGRAM_API_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello word from Python")


@dispatcher.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Write me here something")


@dispatcher.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dispatcher)
