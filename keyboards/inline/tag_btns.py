from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


async def tag_btns(item_code):
    quantity = await db.getQuantityByItemCode(item_code)
    return InlineKeyboardMarkup(

        inline_keyboard=[
            [
                InlineKeyboardButton(text="Kategoriyalarga qaytish", callback_data=f"{item_code}:backToCategories")
            ],
            [
                InlineKeyboardButton(text="-", callback_data=f"{item_code}:decrement"),
                InlineKeyboardButton(text=str(quantity[0]), callback_data=f"{item_code}:value"),
                InlineKeyboardButton(text="+", callback_data=f"{item_code}:increment")

            ],
            [
                InlineKeyboardButton(text="🛒 Savatga qo'shish",
                                     callback_data=f"{item_code}:add_to_cart")
            ],
            [
                InlineKeyboardButton(text="🔙 ortga", callback_data=f"{item_code}:back")
            ]
        ]
    )
