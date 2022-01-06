from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

getLocation_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Joylashuvingizni tasdiqlang",request_location=True)
        ]
    ],resize_keyboard=True, one_time_keyboard=True
)