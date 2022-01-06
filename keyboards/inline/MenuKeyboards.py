from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buy_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍 Xarid qilish", callback_data="buy")
        ]
    ]
)
AgainBuy = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍 Yana xarid qilish", callback_data="buy")
        ]
    ]
)