import uuid
from aiogram import types
from aiogram.types import CallbackQuery, InputFile

from loader import dp, bot, db
from data.config import CHANNELS
from keyboards.inline.Categories import getCategories
from keyboards.inline.subCategories import subCategory
from keyboards.inline.tag_btns import tag_btns
from keyboards.default.getContact import getContactNum
from keyboards.default.getLocation import getLocation_btn
from keyboards.inline.MenuKeyboards import buy_btn, AgainBuy
from keyboards.inline.cartButton import CartButtons
from .getLocation import defineLocation
from keyboards.inline.formatPhoneNum import formatPhoneNumber
from keyboards.inline.location_options import locationOptionButtons


@dp.callback_query_handler(text='buy')
async def control_user(call: types.CallbackQuery, again=False):
    Category_btns = await getCategories()
    if not again:
        await call.message.delete()
        await call.message.answer("Kategoriyalarni tanlang: ", reply_markup=Category_btns)
    else:
        await call.message.answer(text="Buyurtmangiz qabul qilindi tez orada mahsulotingiz "
                                       "yetkazib beriladi",
                                  reply_markup=Category_btns)


@dp.callback_query_handler(text="my_cart")
async def openCart(call: CallbackQuery):
    try:
        await call.message.delete()
        user_id = call.from_user.id
        cart_id = await db.get_cart_id(user_id)
        cartItems = await db.getAllCartItems(cart_id)
        details = []
        text = "Sizning savatchangiz:\n\n"
        calc = ""
        for item in cartItems:
            product = await db.getProductName(item[1])
            text += f"Mahsulot nomi: {product[0]} x {item[0]} \n"
            details.append((product[1] * item[0]))
            calc += f"{item[0]} x {'{:,}'.format(product[1])} = {'{:,}'.format(product[1] * item[0])} sum\n"
        text += '\n' + calc + f"\n💰Jami: {'{:,}'.format(sum(details))} sum"
        btn = await CartButtons(cartItems, cart_id)
        await call.message.answer(text=text, reply_markup=btn)

    except Exception as e:
        print(e)
        await call.message.answer("Sizning savatchangiz bo'sh! Xarid qilishni boshlash uchun quyidagi tugmadan "
                                  "foydalaning", reply_markup=buy_btn)


@dp.callback_query_handler(text_endswith=":removeCartItem")
async def removeItem(call: types.CallbackQuery):
    item_code = call.data.split(":")[0]
    await db.RemoveCartItem(item_code)
    await openCart(call)


@dp.callback_query_handler(text_endswith=":decrement-cartItem")
async def DecreaseQuantity(call: types.CallbackQuery):
    item_code = call.data.split(":")[0]
    quantity = await db.getQuantityByItemCode(item_code)
    if quantity[0] > 1:
        new_quantity = quantity[0] - 1
        await db.update_quantity(quantity=new_quantity, item_code=item_code)
    elif quantity[0] == 1:
        await db.RemoveCartItem(item_code)
    await openCart(call)


@dp.callback_query_handler(text_endswith=":increment-cartItem")
async def IncreaseQuantity(call: types.CallbackQuery):
    item_code = call.data.split(":")[0]
    quantity = await db.getQuantityByItemCode(item_code)
    new_quantity = quantity[0] + 1
    await db.update_quantity(quantity=new_quantity, item_code=item_code)
    await openCart(call)


@dp.callback_query_handler(text_endswith=":backToCategories")
async def reduceProducts(call: types.CallbackQuery):
    item_code = call.data.split(":")[0]
    await db.RemoveCartItem(item_code=item_code)
    await call.message.delete()
    Category_btns = await getCategories()
    await call.message.answer(text="Qaysi kategoriyani tanlaysiz?",
                              reply_markup=Category_btns)


async def sendCartOrder(user_id):
    getname = await db.getNameAndPhone(user_id)
    location = await db.getUserLocation(user_id)
    phone = getname[1]
    fullname = getname[0]
    cart_id = await db.get_cart_id(user_id)
    text = f"Mahsulotlar:\n\n<b>Buyurtma raqami:</b> #{cart_id[0]}\n\n"

    cartItems = await db.getAllCartItems(cart_id)
    details = []
    calc = ""
    for item in cartItems:
        product = await db.getProductName(item[1])
        await db.giveOrder(user_id=user_id, product_id=item[1], quantity=item[0])
        text += f"Mahsulot nomi: {product[0]} x {item[0]} ta\n"
        details.append((product[1] * item[0]))
        calc += f"{'{:,}'.format(product[1])}x{item[0]} = {'{:,}'.format(product[1] * item[0])} sum\n"
    text += '\n' + calc + f"\n💰Jami: {'{:,}'.format(sum(details))} sum\n\nBuyurtmachi: {fullname}\n\nTel Raqami: {phone}"
    await bot.send_message(CHANNELS[0], text)
    try:
        await bot.send_location(CHANNELS[0], longitude=location[0], latitude=location[1])
    except:
        pass


@dp.callback_query_handler(text="buyNow")
async def buy_now(call: types.CallbackQuery):
    await db.buyAllItems(user_id=call.from_user.id, buyAllItems=True)
    await call.message.delete()
    await call.message.answer(text="Buyurtma qilish uchun telefon raqamingizni quyidagi tugma orqali kiriting.",
                              reply_markup=getContactNum)


@dp.callback_query_handler(text_startswith="category")
async def all_products(call: CallbackQuery):
    category_id = call.data.split(":")[-1]
    btns = await subCategory(category_id=int(category_id), user_id=call.from_user.id)
    await call.message.delete()
    await call.message.answer("Qay birini tanlaydilar?", reply_markup=btns)


@dp.callback_query_handler(text_startswith='product')
async def product_info(call: CallbackQuery):
    user_id = call.from_user.id
    try:
        cart_id = await db.get_cart_id(user_id=user_id)
    except:
        await db.createCart(user_id=user_id)
        cart_id = await db.get_cart_id(user_id=user_id)

    product_id = call.data.split(":")[-1]
    product_id = int(product_id)
    try:
        item_code = await db.getItemCode(cart_id, product_id)
    except:
        item_code = uuid.uuid4()
        item_code = str(item_code)
        await db.createCartItem(quantity=int(0), cart_id=cart_id, product_id=product_id, item_code=item_code)
    product =await db.get_product(product_id)
    product_name = product[0][0]
    description = product[0][1]
    cost = product[0][2]
    overall_text = f"Mahsulot:{product_name}\n💰 Narxi: {cost} sum\n\nMa'lumot: {description}"
    await call.message.delete()
    product_image = db.get_product_image(product_id)
    photo_file = InputFile(path_or_bytesio=f"media/{product_image[0][0]}")
    btn = await tag_btns(item_code)
    await call.message.answer_photo(photo_file, caption=overall_text, reply_markup=btn)


@dp.callback_query_handler(text_endswith=':increment')
async def increment(call: CallbackQuery):
    item_code = call.data.split(":")[0]
    try:
        quantity = await db.getQuantityByItemCode(item_code)
    except:
        quantity = await db.getQuantityByItemCode(item_code[2:-3])
        item_code = item_code[2:-3]
    new_quantity = quantity[0] + 1
    await db.update_quantity(quantity=new_quantity, item_code=item_code)
    btns = await tag_btns(item_code)
    await call.message.edit_reply_markup(reply_markup=btns)


@dp.callback_query_handler(text_endswith=':decrement')
async def decrement(call: CallbackQuery):
    item_code = call.data.split(":")[0]
    quantity = await db.getQuantityByItemCode(item_code)
    if quantity[0] > 0:
        new_quantity = quantity[0] - 1
        await db.update_quantity(quantity=new_quantity, item_code=item_code)
        btns = await tag_btns(item_code)
        await call.message.edit_reply_markup(reply_markup=btns)
    else:
        await call.answer(text="Uzur 0 dan ham kam buyurtma berib bo'lmaydi 😒", show_alert=True)


@dp.callback_query_handler(text_endswith="add_to_cart")
async def add_to_cart(call: CallbackQuery):
    item_code = call.data.split(":")[0]
    quantity = await db.getQuantityByItemCode(item_code)
    print(quantity)
    cart_id = await db.get_cart_id(user_id=call.from_user.id)
    product_id = await db.getProductId(cart_id=cart_id)
    category_id = await db.getProductCategory(product_id)
    if quantity[0] > 0:
        await call.message.delete()
        btns = await subCategory(category_id=int(category_id[0]), user_id=call.from_user.id)
        await call.message.answer(text="Qay birini tanlaydilar?", reply_markup=btns)

    else:
        await call.answer(text="Siz hali miqdorni oshirmadingiz :(", show_alert=True)


@dp.callback_query_handler(text_endswith=":book_now")
async def book_now(call: CallbackQuery):
    cart_id = call.data.split(":")[0]
    quantity = await db.get_quantity(int(cart_id))
    try:
        if quantity[-1][0] > 0:
            await call.message.delete()
            state = await db.getStateShoppedBefore(user_id=call.from_user.id)
            if not state[0]:
                await call.message.answer(text="Buyurtma qilish uchun telefon raqamingizni quyidagi tugma orqali "
                                               "kiriting.", reply_markup=getContactNum)
            else:
                btn = await locationOptionButtons(user_id=call.from_user.id)
                await call.message.answer(text="Qaysi manzilingizni tanlaysiz?", reply_markup=btn)
    except:
        await call.answer(text="Sizning savatchangiz bo'sh avval uni to'ldirish kerak 😊", show_alert=True)


@dp.message_handler(content_types="contact", is_sender_contact=True)
async def getNum(msg: types.Message):
    user_id = msg.from_user.id
    phone = msg.contact.phone_number
    await db.update_phone(user_id=user_id, phone=phone)
    await msg.answer(text="Raqamingiz qabul qilindi. Iltimos joylashuvingizni yuboring",
                     reply_markup=getLocation_btn)


@dp.callback_query_handler(text="addAnotherLocation")
async def addAnotherLocation(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Yangi manzilingizni kiriting", reply_markup=getLocation_btn)


@dp.callback_query_handler(text_startswith="location")
async def chooseLocation(call: CallbackQuery):
    await call.message.delete()
    location_id = call.data.split(":")[-1]
    location_details = await db.getLocationById(location_id=location_id)
    user_id = call.from_user.id
    cart_id = await db.get_cart_id(user_id)
    await sendCartOrder(user_id)
    location = await defineLocation(location_details[1], location_details[0])
    getname = await db.getNameAndPhone(user_id=user_id)
    phone = getname[1]
    text = f"<b>Buyurtmangiz qabul qilindi. Belgilangan vaqt ichida yetkazib beramiz.</b>:\n\n<b>Buyurtma " \
           f"ma’lumotlari:</b>\n\n<b>Buyurtma raqami:</b> #{cart_id[0]}\n\n<b>Tanlangan Mahsulotlar</b>\n\n"
    cartItems = await db.getAllCartItems(cart_id)
    details = []
    counter = 0
    for item in cartItems:
        product = await db.getProductName(item[1])
        await db.giveOrder(user_id=user_id, product_id=item[1], quantity=item[0])
        counter += 1
        text += f"{counter}. {product[0]} -- {'{:,}'.format(product[1])}x{item[0]} = {'{:,}'.format(product[1] * item[0])} \n"
        details.append((product[1] * item[0]))
    text += f"\n<b>💰Jami summa</b>: {'{:,}'.format(sum(details))} so'm\n\n<b>Yetkazib beriladigan manzil: </b>{location}." \
            f"\n<b>Telefon raqam:</b>{formatPhoneNumber(phone)}"
    await db.RemoveAllCartItems(cart_id)
    await db.buyAllItems(user_id, False)
    await db.NoticeShopping(user_id=user_id)
    await call.message.answer(text=text, reply_markup=AgainBuy)


@dp.message_handler(content_types=["location"], is_forwarded=False)
async def getLocation(msg: types.Message):
    user_id = msg.from_user.id
    cart_id = await db.get_cart_id(user_id=user_id)
    product_id = await db.getProductId(cart_id=cart_id)
    getname = await db.getNameAndPhone(user_id=user_id)
    phone = getname[1]
    fullname = getname[0]
    try:
        await db.checkUserLocation(user_id=user_id, latitude=msg.location.latitude, longitude=msg.location.longitude)
    except:
        await db.addUserLocation(user_id=user_id, latitude=msg.location.latitude, longitude=msg.location.longitude)
    location = await defineLocation(msg.location.latitude, msg.location.longitude)
    text = f"<b>Buyurtmangiz qabul qilindi. Belgilangan vaqt ichida yetkazib beramiz.</b>:\n\n<b>Buyurtma " \
           f"ma’lumotlari:</b>\n\n<b>Buyurtma raqami:</b> #{cart_id[0]}\n\n<b>Tanlangan Mahsulotlar</b>\n\n"

    await sendCartOrder(user_id)
    cartItems = await db.getAllCartItems(cart_id)
    details = []
    counter = 0
    for item in cartItems:
        product = await db.getProductName(item[1])
        await db.giveOrder(user_id=user_id, product_id=item[1], quantity=item[0])
        counter += 1
        text += f"{counter}. {product[0]} -- {'{:,}'.format(product[1])}x{item[0]} = {'{:,}'.format(product[1] * item[0])} \n"
        details.append((product[1] * item[0]))
    text += f"\n<b>💰Jami summa</b>: {'{:,}'.format(sum(details))} so'm\n\n<b>Yetkazib beriladigan manzil: </b>{location}." \
            f"\n<b>Telefon raqam:</b>{formatPhoneNumber(phone)}"

    await db.RemoveAllCartItems(cart_id=cart_id)
    await db.RemoveCartByUserId(user_id=user_id)
    await db.buyAllItems(user_id, False)
    await db.NoticeShopping(user_id=user_id)
    await msg.answer(text=text, reply_markup=AgainBuy)


@dp.callback_query_handler(text_endswith=":back")
async def back(msg: types.CallbackQuery):
    user_id = msg.from_user.id
    item_code = msg.data.split(":")[0]
    cart_id = await db.get_cart_id(user_id)
    product_id = await db.getProductId(cart_id=cart_id)
    category_id = await db.getProductCategory(product_id=product_id)
    category_id = category_id[0]
    await db.RemoveCartItem(item_code=item_code)
    btns = await subCategory(category_id, user_id)
    await msg.message.delete()
    await msg.message.answer("Qay birini tanlaydilar?", reply_markup=btns)


@dp.callback_query_handler(text="subcategory-back")
async def subcategory_back(msg: types.Message):
    await control_user(msg)
