from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# Main Menu
main_menu_btn_subscription = KeyboardButton('Подписка')
btn_settings = KeyboardButton('Настройка')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(btn_settings, main_menu_btn_subscription)

# Subscription inline buttons
btn_subscribe = InlineKeyboardButton('Подписаться за 1000 ₽', callback_data="subscribe")

subscription_inline_markup = InlineKeyboardMarkup(row_width=1)
subscription_inline_markup.insert(btn_subscribe)
