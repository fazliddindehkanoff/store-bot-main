from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db


async def CartButtons(cart_items, cart_id):
    products_btn = InlineKeyboardMarkup()

    for item in cart_items:
        item_code = await db.getItemCode(cart_id, item[1])
        product_name = await db.getProductName(item[1])
        products_btn.insert(InlineKeyboardButton(text=f"❌ {product_name[0]}",
                                                 callback_data=f"{item_code[0]}:removeCartItem"))
        products_btn.add(InlineKeyboardButton(text="-", callback_data=f"{item_code[0]}:decrement-cartItem"),

                         InlineKeyboardButton(text=str(item[0]), callback_data=f"{cart_id}:value"),
                         InlineKeyboardButton(text="+", callback_data=f"{item_code[0]}:increment-cartItem"))
    products_btn.add(InlineKeyboardButton(text="🔙 ortga", callback_data=f"{item_code[0]}:add_to_cart"))
    return products_btn
