from django.db import models
from django.core.urlresolvers import reverse
import mptt
from jsonfield import JSONField
from mptt.models import MPTTModel, TreeForeignKey

class ProductCategory(MPTTModel):
    name = models.CharField(db_index=True, unique=True, max_length=64, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=64, db_index=True, unique=True, default=None)
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product''s category'
        verbose_name_plural = 'Category of products'
        ordering = ('tree_id', 'level')

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('products:ProductListByCategory', args=[self.slug])

mptt.register(ProductCategory, order_insertion_py=['name'])

class ProductAttribute(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Product attribute'
        verbose_name_plural = 'Product attributes'

class AttributeChoiceValue(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=64, unique=True)
    attribute = models.ForeignKey(ProductAttribute, related_name='values')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'attribute')
        verbose_name = 'attribute choices value'
        verbose_name_plural = 'attribute choices values'


class ProductClass(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    has_variants = models.BooleanField(default=True)
    # product_attributes = models.ManyToManyField(ProductAttribute, related_name='products_class', blank=True)
    variant_attributes = models.ManyToManyField(ProductAttribute, related_name='variants_class', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product class'
        verbose_name_plural = 'product classes'

class Product(models.Model):
    name = models.CharField(unique=True, max_length=255, db_index=True, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=64, blank=True, null=True, default=None) #(max_length=64, db_index=True, unique=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(db_index=True, blank=True, null=True, default=None)
    short_description = models.TextField(blank=True, null=True, default=None)
    producer = models.CharField(db_index=True, max_length=255, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, verbose_name="image of product")
    discount = models.IntegerField(blank=True, null=True, default=0)
    stock = models.PositiveIntegerField(blank=True, null=True, default=0, verbose_name="In stock")
    category = TreeForeignKey(ProductCategory, blank=True, null=True, default=None, related_name='products')
    product_class = models.ForeignKey(ProductClass, blank=True, null=True, default=None, related_name='products')
    is_active = models.BooleanField(default=True)
    is_hit = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
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
        return reverse('products:Product', args=[self.id, self.slug])

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

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
    image = models.ImageField(upload_to='products_images')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{!s}".format(self.id)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='variants')
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    attributes = JSONField(default={})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
