from django.contrib import admin
from .models import Cart, Category, Client, Product, OrderedItems


admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(OrderedItems)
