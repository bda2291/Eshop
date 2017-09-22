from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import HStoreField
from autoslug import AutoSlugField
import mptt
import decimal
from mptt.models import MPTTModel, TreeForeignKey


class ProductAttribute(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Product attribute'
        verbose_name_plural = 'Product attributes'

class AttributeChoiceValue(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    slug = AutoSlugField(populate_from='name')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'attribute')
        verbose_name = 'attribute choices value'
        verbose_name_plural = 'attribute choices values'

class Producer(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(upload_to='producers/%Y/%m/%d/', blank=True, verbose_name="image of producer")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:CategoriesListByProducer', args=[self.slug])

    class Meta:
        verbose_name = 'Producer'
        verbose_name_plural = 'Producers'

class ProductCategory(MPTTModel):
    name = models.CharField(db_index=True, unique=True, max_length=64, blank=True, null=True, default=None)
    slug = AutoSlugField(populate_from='name')
    is_active = models.BooleanField(default=True)
    producer = models.ForeignKey(Producer, null=True, blank=True, related_name='categories')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', blank=True, verbose_name="image of category")
    # category_attributes = models.ManyToManyField(ProductAttribute, related_name='categories', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product''s category'
        verbose_name_plural = 'Category of products'
        ordering = ('tree_id', 'level')

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('products:ProductListByCategory', args=[self.producer.slug, self.slug])

mptt.register(ProductCategory, order_insertion_py=['name'])

# class ProductClass(models.Model):
#     name = models.CharField(max_length=64, blank=True, null=True, default=None)
#     has_variants = models.BooleanField(default=True)
#     # product_attributes = models.ManyToManyField(ProductAttribute, related_name='products_class', blank=True)
#     variant_attributes = models.ManyToManyField(ProductAttribute, related_name='variants_class', blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'product class'
#         verbose_name_plural = 'product classes'

class Product(models.Model):
    name = models.CharField(max_length=64, db_index=True, blank=True, null=True, default=None)
    slug = AutoSlugField(populate_from='name')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # points = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    description = models.TextField(db_index=True, blank=True, null=True, default=None)
    # short_description = models.TextField(blank=True, null=True, default=None)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="image of product")
    discount = models.IntegerField(blank=True, null=True, default=0)
    stock = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name="In stock")
    # category = TreeForeignKey(ProductCategory, blank=True, null=True, default=None, related_name='products')
    category = models.ForeignKey(ProductCategory, default=None, related_name='products')
    attributes = models.ManyToManyField(ProductAttribute, related_name='categories', blank=True)
    discount_policy = HStoreField(blank=True, null=True, default={})
    is_active = models.BooleanField(default=True)
    # is_hit = models.BooleanField(default=False)
    # is_new = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('products:Product', args=[self.slug])

    # def save(self, *args, **kwargs):
    #     if self.category:
    #         super(Product, self).save(*args, **kwargs)
    #
    #         for cp in ProductClass.objects.filter(category=self.product_class):
    #             pp = ProductProperty.objects.filter(category_property=cp,
    #                                                 product=self)
    #             if not pp:
    #                 pp = ProductProperty(category_property=cp, product=self, value="--")
    #                 pp.save()

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
#     image = models.ImageField(upload_to='products_images')
#     is_main = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     created = models.DateField(auto_now_add=True, auto_now=False)
#     updated = models.DateField(auto_now_add=False, auto_now=True)
#
#     def __str__(self):
#         return "{!s}".format(self.id)
#
#     class Meta:
#         verbose_name = 'Photo'
#         verbose_name_plural = 'Photos'

class Offer(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    slug = AutoSlugField(populate_from='name')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    # points = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                related_name='variants')
    is_active = models.BooleanField(default=True)
    attributes = HStoreField(blank=True, null=True, default={})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'

    def save(self, *args, **kwargs):
        self.points = self.price * decimal.Decimal('0.1')
        super(Offer, self).save(*args, **kwargs)
