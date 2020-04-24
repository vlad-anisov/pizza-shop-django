from django.contrib import admin
from .models import Item, Order, Pizza, Drink, Restaurant, Address

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Drink)
admin.site.register(Pizza)
admin.site.register(Restaurant)
admin.site.register(Address)