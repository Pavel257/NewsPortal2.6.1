from django.db import models

# Create your models here.
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    price = models.FloatField(default=0.0, verbose_name='Стоимость в рублях')

    def __str__(self):
        return self.name + "/" + str(self.price)



    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Время оформления заказа')
    time_out = models.DateTimeField(null=True, verbose_name='Время получения заказа')
    cost = models.FloatField(default=0.0, verbose_name='Цена')
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    products = models.ManyToManyField(Product, through='ProductOrder')

    class Meta:
        verbose_name = "Заказы"
        verbose_name_plural = "Заказы"


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Товары и заказы"
        verbose_name_plural = "Товары и заказы"