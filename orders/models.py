from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
# from discount.models import Discount
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product, Offer


class Status(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'State of order'
        verbose_name_plural = 'States'

class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=64, blank=True, null=True, default=None)
    city = models.CharField(max_length=100, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comment = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, blank=True, null=True, default=None)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    paid = models.BooleanField(default=False)
    # discount = models.ForeignKey(Discount, related_name='orders', null=True, blank=True)
    # discount_value = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    points_quant = models.IntegerField(default=0)

    def __str__(self):
        return "Order {!s} has status {}: ".format(self.id, self.status)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductsInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, related_name='items')
    product = models.ForeignKey(Offer, blank=True, null=True, default=None)
    number = models.PositiveIntegerField(default=1)
    price_per_itom = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Product in Order'
        verbose_name_plural = 'Products in Order'

    def save(self, *args, **kwargs):
        # self.price_per_itom = self.product.price
        self.total_price = self.number * self.price_per_itom
        super(ProductsInOrder, self).save(*args, **kwargs)

class ProductsInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    number = models.IntegerField(default=1)
    price_per_itom = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Product in Cart'
        verbose_name_plural = 'Products in Cart'

    def save(self, *args, **kwargs):
        self.price_per_itom = self.product.price
        self.total_price = int(self.number) * self.price_per_itom
        super(ProductsInBasket, self).save(*args, **kwargs)

@receiver(post_save, sender=ProductsInOrder)
def product_in_order_post_save(instance,**kwargs):
    order = instance.order
    all_products_in_order = ProductsInOrder.objects.filter(order=order, is_active=True)

    order_total_price = sum(item.total_price for item in all_products_in_order)
    # if order.discount:
    #     order.total_price = order_total_price * (order.discount_value / Decimal('100'))
    if order.points_quant:
        order.total_price = order_total_price - order.points_quant
    else:
        order.total_price = order_total_price
    order.save(force_update=True)
