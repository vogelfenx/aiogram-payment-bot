import logging
from enum import Enum

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, storage
from aiogram.types import message
from aiogram.types.message import ContentType
from aiogram.utils import executor

import config
import navbar
import services

logging.basicConfig(level=logging.INFO)

payment_states = Enum('states', ('PAID', 'NOT_PAID'))

bot = Bot(config.TELEGRAM_API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


@dispatcher.message_handler(state='*', commands=['start'])
async def process_start_command(message: types.Message):
    state = dispatcher.current_state(user=message.from_user.id)
    await state.set_state(payment_states.NOT_PAID.name)
    await message.reply("Выбери в меню 'Подписка' для дальнейшего использования",
                        reply_markup=navbar.main_menu)


@dispatcher.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Бот отвечает на любой вопрос случайной гифкой")


@dispatcher.message_handler(state=payment_states.NOT_PAID.name)
async def offer_subscription(message: types.Message):
    """Offer subscription"""
    if message.chat.type == 'private':
        state = dispatcher.current_state(user=message.from_user.id)
        if message.text == navbar.main_menu_btn_subscription.text:
            await message.reply('Подпишись на бота для дальнейшего использования',
                                reply_markup=navbar.subscription_inline_markup,
                                reply=False)


@dispatcher.callback_query_handler(state=payment_states.NOT_PAID.name, text='subscribe')
async def subscribe(call: types.CallbackQuery):
    """Send payment invoice"""
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id,
                           text='Используй для теста карту:\n1111 1111 1111 1026\n11/21\nCVC: 000 ')
    await bot.send_invoice(chat_id=call.from_user.id,
                           title='Подписка на канал',
                           description='Подписка на канал за 1000 рублей',
                           payload='channel_subscription',
                           provider_token=config.YOOKASSA_TEST_PAYMENT_TOKEN,
                           currency="RUB",
                           start_parameter='test_bot',
                           prices=[{"label": "Руб", "amount": 100000}])


@dispatcher.pre_checkout_query_handler(state=payment_states.NOT_PAID.name)
async def process_pre_checkout_query(pre_checkput_query: types.PreCheckoutQuery):
    """Do final confirmation to complete payment process."""
    await bot.answer_pre_checkout_query(pre_checkput_query.id, ok=True)


@dispatcher.message_handler(state=payment_states.NOT_PAID.name, content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_payment(message: types.Message):
    """Process successful payment."""
    if message.successful_payment.invoice_payload == 'channel_subscription':
        state = dispatcher.current_state(user=message.from_user.id)
        await state.set_state('PAID')
        await bot.send_message(message.from_user.id, "Подписка оформлена. Напиши любой вопрос.")


@dispatcher.message_handler(state=payment_states.PAID.name)
async def send_yes_or_no_image(message: types.Message):
    """Answer yes or no using yes / no wtf api"""
    image_url = services.fetch_yes_or_no_image()
    await bot.send_animation(message.from_user.id, image_url)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
