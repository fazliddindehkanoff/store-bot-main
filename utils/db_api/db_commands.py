import psycopg2
from data import config
import datetime


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS
        )

    async def add_user(self, full_name, phone, username, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into storebot_client (fullname, phone, username, user_id, buy_all_items, "
                           " shopped_before) "
                           "values (%s, %s, %s, %s, %s, %s)",
                           (full_name, phone, username, user_id, 'false', 'false'))
            self.connection.commit()

    async def RemoveUser(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from storebot_client where user_id = %s", (user_id,))
            self.connection.commit()

    async def NoticeShopping(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("update storebot_client set shopped_before = true where user_id = %s", (user_id,))
            self.connection.commit()

    async def getStateShoppedBefore(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select shopped_before from storebot_client where user_id = %s", (user_id,))
            state = cursor.fetchone()
        return state

    async def RemoveCartByUserId(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from storebot_cart where client_user_id = %s", (user_id,))
            self.connection.commit()

    async def addUserLocation(self, user_id, longitude, latitude):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into storebot_clientlocations (longitude, latitude, client_id, created_at) values("
                           "%s,%s,%s,%s)",
                           (longitude, latitude, user_id, datetime.datetime.now()))
            self.connection.commit()

    async def checkUserLocation(self, user_id, longitude, latitude):
        with self.connection.cursor() as cursor:
            cursor.execute("select id from storebot_clientlocations where client_id = %s and longitude = %s and "
                           "latitude = %s", (str(user_id), str(longitude), str(latitude)))
            result = cursor.fetchone()
        if result is None:
            raise Exception
        else:
            return result

    async def getLocationById(self, location_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select longitude, latitude from storebot_clientlocations where id = %s", (location_id,))
            location = cursor.fetchone()
        return location

    async def getUserLocation(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select longitude, latitude from storebot_clientlocations where client_id = %s order by "
                           "created_at",
                           (str(user_id),))
            location = cursor.fetchone()
        return location

    async def getAllLocations(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select id, longitude, latitude from storebot_clientlocations where client_id = %s", (str(user_id),))
            locations = cursor.fetchall()
        return locations

    async def checkUser(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select user_id from storebot_client where user_id = %s", (user_id,))
            user = cursor.fetchone()
        if user is None:
            raise Exception

    async def buyAllItems(self, user_id, buyAllItems):
        with self.connection.cursor() as cursor:
            cursor.execute("update storebot_client set buy_all_items = %s where user_id = %s", (buyAllItems, user_id))
            self.connection.commit()

    async def getBuyState(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select buy_all_items from storebot_client where user_id = %s", (user_id,))
            state = cursor.fetchone()
        return state

    async def getNameAndPhone(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select fullname, phone from storebot_client where user_id = %s", (user_id,))
            NameAndPhone = cursor.fetchone()
        return NameAndPhone

    async def update_phone(self, user_id, phone):
        with self.connection.cursor() as cursor:
            cursor.execute("update storebot_client set phone = %s where user_id = %s", (phone, user_id))
            self.connection.commit()

    def get_all_categories(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select id, category_name from storebot_category")
            row = cursor.fetchall()
        return row

    def get_subcategories(self, category_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select product_name, id from storebot_product where category_id = %s", (category_id,))
            products = cursor.fetchall()
        return products

    def get_product(self, product_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select product_name, description, price from storebot_product where id = %s", (product_id,))
            products = cursor.fetchall()
        return products

    async def getProductCategory(self, product_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select category_id from storebot_product where id = %s", (product_id,))
            category_id = cursor.fetchone()
        return category_id

    async def getProductName(self, product_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select product_name, price from storebot_product where id = %s", (product_id,))
            name = cursor.fetchone()
        return name

    def get_product_image(self, product_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select product_image from storebot_product where id = %s", (product_id,))
            product_image = cursor.fetchall()
        return product_image

    async def createCart(self, user_id,):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into storebot_cart (client_user_id)"
                           "values (%s)", (user_id,))
            self.connection.commit()
            cursor.execute("select id from storebot_cart where client_user_id = %s", (user_id,))
            cart_id = cursor.fetchone()
        return cart_id

    async def get_cart_id(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select id from storebot_cart where client_user_id = %s", (user_id,))
            cart_id = cursor.fetchone()
        if cart_id is None:
            raise Exception
        else:
            return cart_id

    async def createCartItem(self, quantity, cart_id, product_id, item_code):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into storebot_cartitem (quantity, cart_id, product_id, item_code)"
                           " values (%s, %s, %s, %s)", (quantity, cart_id, product_id, item_code))
            self.connection.commit()

    async def giveOrder(self, quantity, user_id, product_id):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into storebot_ordereditems (quantity, user_id, product_id)"
                           "values (%s, %s, %s)", (quantity, user_id, product_id))
            self.connection.commit()

    async def giveOrderForAllItems(self, cart_id):
        with self.connection.cursor() as cursor:
            cursor.execute("")

    async def getAllCartItems(self, cart_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select quantity, product_id, item_code from storebot_cartitem where cart_id = %s ",
                           (cart_id,))
            cart_items = cursor.fetchall()
        if not cart_items:
            raise Exception
        else:
            return cart_items

    async def getQuantityByItemCode(self, item_code):
        with self.connection.cursor() as cursor:
            cursor.execute("select quantity from storebot_cartitem where item_code = %s",
                           (item_code,))
            quantity = cursor.fetchone()
        if quantity is None:
            raise Exception
        else:
            return quantity

    async def getItemCode(self, cart_id, product_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select item_code from storebot_cartitem where cart_id = %s and"
                           " product_id = %s", (cart_id, product_id))
            item_code = cursor.fetchone()
        if item_code is None:
            raise Exception
        else:
            return item_code

    async def addToActiveCartItems(self, product_id, cart_id, quantity, item_code):
        with self.connection.cursor() as cursor:
            cursor.execute("insert into storebot_activecartitems (product_id, cart_id, quantity, item_code)")

    async def RemoveCartItem(self, item_code):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from storebot_cartitem where item_code = %s", (item_code,))
            self.connection.commit()

    async def RemoveAllCartItems(self, cart_id):
        with self.connection.cursor() as cursor:
            cursor.execute("delete from storebot_cartitem where cart_id = %s", (cart_id,))
            self.connection.commit()

    async def getProductId(self, cart_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select product_id from storebot_cartitem where cart_id = %s", (cart_id,))
            product_id = cursor.fetchone()
        return product_id

    async def getSameProducts(self, product_id, cart_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select quantity, item_code from storebot_cartitem where cart_id = %s and product_id = %s",
                           (cart_id, product_id))
            quantity = cursor.fetchall()
        return quantity

    async def get_quantity(self, cart_id):
        with self.connection.cursor() as cursor:
            cursor.execute("select quantity, product_id from storebot_cartitem where cart_id = %s", (cart_id,))
            quantityAndProductId = cursor.fetchall()
        return quantityAndProductId

    async def update_quantity(self, quantity, item_code):
        with self.connection.cursor() as cursor:
            cursor.execute("update storebot_cartitem set quantity = %s where item_code = %s",
                           (quantity, item_code))
            self.connection.commit()
