import os
import uuid

from django.db import models


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("images", filename)


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    description = models.TextField(verbose_name="Mahsulot haqida", blank=True)
    price = models.IntegerField(verbose_name="Narxi", default=0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, verbose_name="Kategoriyasi")
    is_active = models.BooleanField(verbose_name="Mavjudligi", default=True, null=True)
    product_image = models.ImageField(verbose_name="Mahsulat rasmi", upload_to=get_file_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan sana")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return f"{self.product_name} - {self.category}"


class Client(models.Model):
    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"

    fullname = models.CharField(verbose_name="To'liq ismi", max_length=255, blank=True)
    phone = models.CharField(verbose_name="Telefon raqami", max_length=15, null=True)
    user_id = models.IntegerField(verbose_name="Telegram foydalanuvchi IDsi", default=0, unique=True)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    buy_all_items = models.BooleanField(verbose_name="Barcha narsani sotib oladimi?", default=False)
    shopped_before = models.BooleanField(verbose_name="Avval biron narsa harid qilganmi?", default=False)

    def __str__(self):
        return f"{self.user_id} - {self.fullname}"


class clientLocations(models.Model):
    client_id = models.IntegerField(verbose_name="User_id")
    longitude = models.CharField(verbose_name="Longitude", max_length=255)
    latitude = models.CharField(verbose_name="Latitude", max_length=255)
    created_at = models.DateTimeField(verbose_name="Kiritildi", auto_now_add=True)


class Cart(models.Model):
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    client_user_id = models.IntegerField(verbose_name="Mijozning telegram IDsi", unique=True)

    created_at = models.DateTimeField(verbose_name="Kiritildi", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="O'zgartirildi", auto_now=True, null=True)

    def __str__(self):
        client = Client.objects.filter(user_id=self.client_user_id)
        if client.exists():
            client = client.first()
            return client.fullname
        else:
            return self.client_user_id


class OrderedItems(models.Model):
    class Meta:
        verbose_name = "Buyurtma qilngan mahsulot"
        verbose_name_plural = "Buyurtma qilngan mahsulotlar"
    product = models.ForeignKey(Product, verbose_name="Mahsulot", on_delete=models.CASCADE)
    user_id = models.IntegerField(verbose_name="Client telegram Id si")
    quantity = models.IntegerField(verbose_name="Miqdori")


class CartItem(models.Model):
    class Meta:
        verbose_name = "Buyurtma jihoz"
        verbose_name_plural = "Buyurtma jihozlar"

    product = models.ForeignKey(Product, verbose_name="Mahsulot", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Miqdori")

    item_code = models.CharField(verbose_name="buyurtma kodi", max_length=36)
    created_at = models.DateTimeField(verbose_name="Kiritildi", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="O'zgartirildi", auto_now=True, null=True)

    def __str__(self):
        client = Client.objects.filter(user_id=self.cart.client_user_id)
        if client.exists():
            client = client.first()
            return f"{self.product} - {self.quantity} - {client.fullname}"
        else:
            return f"{self.product} - {self.quantity}"
