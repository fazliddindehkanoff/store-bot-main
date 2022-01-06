# from aiogram import types
# from loader import dp, bot

# from handlers.users.start import bot_start
# from data.config import CHANNELS
# from keyboards.default.getLocation import getLocation_btn
# from .statehandlers import choosen_product

# @dp.message_handler(content_types="contact", is_sender_contact=True)
# async def getNum(msg: types.Message):
#     await bot.send_message(chat_id=CHANNELS[0], text=f"Yangi buyurtma:{choosen_product} \nBuyurtmachi:{msg.contact.full_name}\nbuyurtmachi raqami:{msg.contact.phone_number}")
#     await msg.answer(text="Raqamingiz qabul qilindi. Iltimos joylashuvingizni yuboring",reply_markup=getLocation_btn)

# @dp.message_handler(content_types="location", is_forwarded=False)
# async def getLocation(msg: types.Message):
#     await bot.send_location(chat_id=CHANNELS[0],latitude=msg.location.latitude, longitude=msg.location.longitude)
#     await bot_start(msg, again="again")