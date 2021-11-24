import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils import executor
import navbar

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(config.TELEGRAM_API_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello word from Python",
                        reply_markup=navbar.main_menu)


@dispatcher.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Write me here something")


@dispatcher.message_handler()
async def offer_subscription(message: types.Message):
    """Offer subscrbtion"""
    if message.chat.type == 'private':
        if message.text == navbar.main_menu_btn_subscription.text:
            await message.reply('Подпишись на бота для дальнейшего использования',
                                reply_markup=navbar.subscription_inline_markup,
                                reply=False)


@dispatcher.callback_query_handler(text='subscribe')
async def subscribe(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_invoice(chat_id=call.from_user.id,
                           title='Подписка на канал',
                           description='Подписка на канал за 1000 рублей',
                           payload='channel_subscription',
                           provider_token=config.YOOKASSA_TEST_PAYMENT_TOKEN,
                           currency="RUB",
                           start_parameter='test_bot',
                           prices=[{"label": "Руб", "amount": 100000}])


@dispatcher.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkput_query: types.PreCheckoutQuery):
    """Do final confirmation to complete payment process"""
    await bot.answer_pre_checkout_query(pre_checkput_query.id, ok=True)


@dispatcher.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    if message.successful_payment.invoice_payload == 'channel_subscription':
        await bot.send_message(message.from_user.id, "Оплата успешно прошла. Подписка оформлена")

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
