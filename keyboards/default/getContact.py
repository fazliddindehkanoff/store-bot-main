from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

getContactNum = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📲 Raqamingizni tasdiqlang", request_contact=True)
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)
