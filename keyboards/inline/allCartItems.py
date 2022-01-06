from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from .callback_data import product_callback


async def AllItemBtn(cart_items):
    products_btn = InlineKeyboardMarkup(row_width=1)
    for item in cart_items:
        product_name = await db.getProductName(item[1])
        products_btn.insert(InlineKeyboardButton(text=product_name[0],
                                                 callback_data=product_callback.new(item_code=item[1])))

    return products_btn
