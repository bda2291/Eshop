from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = ProductCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'discount','stock', 'is_active']
    inlines = [ProductImageInline]
    list_filter = ['is_active', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'is_active', 'discount']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    class Meta:
        model = Product

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
