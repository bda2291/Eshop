from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import *

class CustomModelResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        try:
            row['attributes'] = eval(row['attributes'])
        except:
            try:
                row['discount_policy'] = eval(row['discount_policy'])
            except:
                pass

class CustomManyToManyWidget(widgets.ManyToManyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        t1 = super(CustomManyToManyWidget, self).clean(value)
        return self.model.objects.get(name=t1) if t1 else None


# class CustomForeignKeyWidget(widgets.ForeignKeyWidget):
#     def clean(self, value, row=None, *args, **kwargs):
#         return self.model.objects.get_or_create(name=value)[0]

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
    # prepopulated_fields = {'slug': ('name',)}
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
    # prepopulated_fields = {'slug': ('name',)}

    suit_form_tabs = (('general', 'General'),
                      ('ACV', 'AttributeValues'),)

    class Meta:
        model = ProductAttribute

admin.site.register(ProductAttribute, ProductAttributeAdmin)

class ProducerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Producer._meta.fields]

    class Meta:
        model = Producer

admin.site.register(Producer, ProducerAdmin)

class ProductResource(CustomModelResource):
    # id = fields.Field(default=generate_Jid(prefix='J'),
    #                   readonly=True,
    #                   widget=widgets.CharWidget(),
    #                   )

    name = fields.Field(column_name='name', attribute='name',
                        default=None,
                        widget=widgets.CharWidget(),
                        )
    # price = fields.Field(column_name='price', attribute='price',
    #                      default=0,
    #                      widget=widgets.DecimalWidget(),
    #                      )
    description = fields.Field(column_name='description', attribute='description',
                               default=None,
                               widget=widgets.CharWidget(),
                               )

    # producer = fields.Field(column_name='producer', attribute='producer',
    #                     default=None,
    #                     widget=widgets.CharWidget(),
    #                     )

    category = fields.Field(column_name='category', attribute='category',
                            default=None,
                            widget=widgets.ForeignKeyWidget(ProductCategory, field='name'),
                            )
    producer = fields.Field(column_name='producer', attribute='producer',
                            default=None,
                            widget=widgets.ForeignKeyWidget(Producer, field='name'),
                            )
    attributes = fields.Field(column_name='attributes', attribute='attributes',
                            default=None,
                            widget=CustomManyToManyWidget(ProductAttribute, field="name"),
                            )
    is_active = fields.Field(column_name='is_active', attribute='is_active',
                           default=1,
                           widget=widgets.BooleanWidget())

    discount_policy = fields.Field(column_name='discount_policy', attribute='discount_policy',
                               default={},
                               widget=widgets.CharWidget())

    # delete = fields.Field(column_name='delete', attribute='delete',
    #                       default=0,
    #                       widget=widgets.BooleanWidget())

    # def for_delete(self, row, instance):
    #     return self.fields['delete'].clean(row)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'producer', 'category', 'is_active', 'attributes', 'discount_policy')
        export_order = ('id', 'name', 'producer', 'is_active', 'category', 'attributes', 'description', 'discount_policy')
        # import_id_fields = ('name',)

    def dehydrate_str_choices(self, obj):
        if obj.id:
            return obj.str_choices()

class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'category', 'producer', 'is_active']
    inlines = [OfferInline]
    list_filter = ['is_active', 'created', 'updated', 'category']
    list_editable = ['is_active']
    # prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'id']

    suit_form_tabs = (('general', 'General'),
                      ('offers', 'Offers'),)

    resource_class = ProductResource

    # class Meta:
    #     model = Product

class OfferResource(CustomModelResource):
    name = fields.Field(column_name='name', attribute='name',
                        default=None,
                        widget=widgets.CharWidget(),
                        )

    price = fields.Field(column_name='price', attribute='price',
                         default=0,
                         widget=widgets.DecimalWidget(),
                         )

    product = fields.Field(column_name='product', attribute='product',
                            widget=widgets.ForeignKeyWidget(Product, field='name'),
                            )

    is_active = fields.Field(column_name='is_active', attribute='is_active',
                             default=1,
                             widget=widgets.BooleanWidget())

    attributes = fields.Field(column_name='attributes', attribute='attributes',
                               default={},
                             widget=widgets.CharWidget())

    class Meta:
        model = Offer
        fields = ('name', 'product', 'price', 'is_active', 'attributes')
        export_order = ('name', 'product', 'attributes', 'is_active', 'price')
        import_id_fields = ('name',)

class OfferAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'product', 'price', 'is_active', 'attributes']
    resource_class = OfferResource
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ProductImage._meta.fields]
#
#     class Meta:
#         model = ProductImage

# admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
