from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db
from handlers.users.getLocation import defineLocation
from .callback_data import locationOptions_callback


async def locationOptionButtons(user_id):
    locationOptions = InlineKeyboardMarkup(row_width=1)
    locations = await db.getAllLocations(user_id)
    for location in locations:
        location_name = await defineLocation(location[2], location[1])
        locationOptions.insert(InlineKeyboardButton(text=location_name,
                                                    callback_data=locationOptions_callback.new(
                                                        location_id=location[0])))
    locationOptions.insert(InlineKeyboardButton(text="Boshqa manzil kiritish", callback_data="addAnotherLocation"))
    return locationOptions
