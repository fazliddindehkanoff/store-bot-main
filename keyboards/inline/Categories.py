from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from .callback_data import category_callback

Category_btns = InlineKeyboardMarkup(row_width=1)

rows = db.get_all_categories()
for row in rows:
    Category_btns.insert(InlineKeyboardButton(text=row[1], callback_data=category_callback.new(item_code=row[0])))
