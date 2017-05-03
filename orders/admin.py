from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.html import format_html
import csv
import datetime
from .models import *

def OrderDetail(obj):
    return format_html('<a href="{}">View</a>'.format(
        reverse('orders:AdminOrderDetail', args=[obj.id])
    ))

def ExportToCSV(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Orders-{}.csv'.format(datetime.datetime.now().strftime("%d/%m/%Y"))
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)
        writer.writerow(data_row)
    return response
    ExportToCSV.short_description = 'Export CSV'

class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 0

class StatusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Status._meta.fields]

    class Meta:
        model = Status

class OrderAdmin (admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'customer_phone', 'city', 'customer_address',
                    'paid', 'status', 'created', 'updated', OrderDetail]

    list_filter = ['paid', 'created', 'updated']
    inlines = [ProductsInOrderInline]
    actions = [ExportToCSV]

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