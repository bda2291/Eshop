from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = ProductCategory

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
    # delete = fields.Field(column_name='delete', attribute='delete',
    #                       default=0,
    #                       widget=widgets.BooleanWidget())

    # def for_delete(self, row, instance):
    #     return self.fields['delete'].clean(row)

    class Meta:
        model = Product
        exclude = ('slug', 'short_description', 'image', 'is_active', 'created', 'updated')
        # import_id_fields = ('name', 'price', 'description', 'discount', 'stock', 'category', 'delete')

class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'discount','stock', 'is_active']
    inlines = [ProductImageInline]
    list_filter = ['is_active', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'is_active', 'discount']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    resource_class = ProductResource

    # class Meta:
    #     model = Product

class ProductImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductImage._meta.fields]

    class Meta:
        model = ProductImage

admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
