from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from .callback_data import product_callback


async def subCategory(category_id, user_id):
    try:
        cart_id = await db.get_cart_id(user_id=user_id)
    except:
        cart_id = await db.createCart(user_id=user_id)
    subCategory_btn = InlineKeyboardMarkup(row_width=2)
    products = db.get_subcategories(category_id)
    subCategory_btn.insert(InlineKeyboardButton(text="📥 Savat:", callback_data="my_cart"))
    subCategory_btn.insert(InlineKeyboardButton(text="Savatni to’ldirdim ✅", callback_data=f"{cart_id[0]}:book_now"))
    for product in products:
        subCategory_btn.insert(InlineKeyboardButton(text=product[0],
                                                    callback_data=product_callback.new(item_code=product[1])))
    subCategory_btn.insert(InlineKeyboardButton(text="🔙 ortga", callback_data="subcategory-back"))
    return subCategory_btn

