from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.Categories import getCategories
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, again="No"):
    user_id = message.from_user.id
    try:
        await db.checkUser(user_id=user_id)
        await db.RemoveUser(user_id=user_id)
        cart_id = await db.get_cart_id(user_id)
        await db.RemoveAllCartItems(cart_id)
        await db.RemoveCartByUserId(user_id=user_id)
        await db.add_user(
            full_name=message.from_user.full_name,
            phone=0,
            username=message.from_user.username,
            user_id=message.from_user.id
        )

    except Exception as e:
        await db.add_user(
            full_name=message.from_user.full_name,
            phone=0,
            username=message.from_user.username,
            user_id=message.from_user.id
        )
        await db.buyAllItems(user_id=message.from_user.id, buyAllItems=False)
    Category_btns = await getCategories()
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!"
                         f" bizning onlayn do'konimizga xush kelibsiz.", reply_markup=Category_btns)
