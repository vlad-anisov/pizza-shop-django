from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel

payment_CHOICES = (
    ('H', 'Cash'),
    ('D', 'Card'),
)

PIZZA_SIZE_CHIOICES = (
    ('25', 'Small'),
    ('30', 'Medium'),
    ('35', 'Large'),
)

PIZZA_DOUGH_CHIOICES = (
    ('TR', 'Traditional'),
    ('TH', 'Thin'),
)


class Item(PolymorphicModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    photo = models.ImageField(
        upload_to='item', null=True, blank=True)
    price = models.FloatField()

    def __str__(self):
        return self.title


class Drink(Item):

    def __str__(self):
        return f'{self.title} {self.description}'


class Pizza(Item):
    size = models.CharField(choices=PIZZA_SIZE_CHIOICES, max_length=2)
    fats = models.FloatField()
    proteins = models.FloatField()
    carbohydrates = models.FloatField()
    energy_value = models.FloatField()
    weight = models.IntegerField()

    def __str__(self):
        return f'{self.title} {self.size} см'


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.item} {self.quantity} шт'


class Address(models.Model):
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10)


class Restaurant(models.Model):
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.street} {self.house}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        primary_key=True
    )
    order_time = models.DateTimeField()
    order_items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    comment = models.CharField(max_length=100, null=True, blank=True)
