from django.contrib import admin
from .models import *

# Register your models here.

class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 0

class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status

class OrderAdmin (admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductsInOrderInline]
    class Meta:
        model = Order

class ProductsInOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductsInOrder._meta.fields]

    class Meta:
        model = ProductsInOrder

class ProductsInBasketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductsInBasket._meta.fields]

    class Meta:
        model = ProductsInBasket

admin.site.register(Status, StatusAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductsInOrder, ProductsInOrderAdmin)
admin.site.register(ProductsInBasket, ProductsInBasketAdmin)