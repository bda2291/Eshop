from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import *


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 0

# class ProductAttributeInline(admin.TabularInline):
#     model = ProductAttribute
#     extra = 1
#     verbose_name_plural = 'ProductAttribute'
#     suit_classes = 'suit-tab suit-tab-PA'
#
class AttributeChoiceValueInline(admin.TabularInline):
    model = AttributeChoiceValue
    prepopulated_fields = {'slug': ('name',)}
    extra = 1
    verbose_name_plural = 'AttributeChoiceValue'
    suit_classes = 'suit-tab suit-tab-ACV'
#
class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1
    verbose_name_plural = 'Offers'
    suit_classes = 'suit-tab suit-tab-offers'

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = ProductCategory

# class AttributeChoiceValueAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ProductCategory._meta.fields]
#
#     class Meta:
#         model = AttributeChoiceValue
#
# admin.site.register(AttributeChoiceValue, AttributeChoiceValueAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductAttribute._meta.fields]
    inlines = [AttributeChoiceValueInline]
    prepopulated_fields = {'slug': ('name',)}

    suit_form_tabs = (('general', 'General'),
                      ('ACV', 'AttributeValues'),)

    class Meta:
        model = ProductAttribute

admin.site.register(ProductAttribute, ProductAttributeAdmin)

class ProductClassAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductClass._meta.fields]

    class Meta:
        model = ProductClass

admin.site.register(ProductClass, ProductClassAdmin)

class ProductResource(resources.ModelResource):
    # id = fields.Field(default=generate_Jid(prefix='J'),
    #                   readonly=True,
    #                   widget=widgets.CharWidget(),
    #                   )

    name = fields.Field(column_name='name', attribute='name',
                        default=None,
                        widget=widgets.CharWidget(),
                        )
    price = fields.Field(column_name='price', attribute='price',
                         default=0,
                         widget=widgets.DecimalWidget(),
                         )
    description = fields.Field(column_name='description', attribute='description',
                               default=None,
                               widget=widgets.CharWidget(),
                               )
    discount = fields.Field(column_name='discount', attribute='discount',
                            default=0,
                            widget=widgets.IntegerWidget(),
                            )
    stock = fields.Field(column_name='stock', attribute='stock',
                         default=0,
                         widget=widgets.IntegerWidget(),
                         )
    category = fields.Field(column_name='category', attribute='category',
                            widget=widgets.ForeignKeyWidget(ProductCategory, 'name'),
                            )
    is_active = fields.Field(column_name='is_active', attribute='is_active',
                           default=1,
                           widget=widgets.BooleanWidget())
    is_hit = fields.Field(column_name='is_hit', attribute='is_hit',
                             default=0,
                             widget=widgets.BooleanWidget())
    is_new = fields.Field(column_name='is_new', attribute='is_new',
                             default=0,
                             widget=widgets.BooleanWidget())
    # delete = fields.Field(column_name='delete', attribute='delete',
    #                       default=0,
    #                       widget=widgets.BooleanWidget())

    # def for_delete(self, row, instance):
    #     return self.fields['delete'].clean(row)

    class Meta:
        model = Product
        exclude = ('slug', 'short_description', 'image', 'is_active', 'created', 'updated')
        # import_id_fields = ('name', 'price', 'description', 'discount', 'stock', 'category', 'delete')
        model = Offer

class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'discount','stock', 'is_active']
    inlines = [OfferInline]
    list_filter = ['is_active', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'is_active', 'discount']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'id']

    suit_form_tabs = (('general', 'General'),
                      ('offers', 'Offers'),)

    resource_class = ProductResource

    # class Meta:
    #     model = Product

# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ProductImage._meta.fields]
#
#     class Meta:
#         model = ProductImage

# admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
