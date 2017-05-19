import datetime
from haystack import indexes
from .models import *

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name="search/product_text.txt")
    name = indexes.EdgeNgramField(model_attr='name')
    description = indexes.EdgeNgramField(model_attr='description')
    category = indexes.CharField(model_attr='category', faceted=True)
    producer = indexes.CharField(model_attr='producer', faceted=True)

    content_auto = indexes.EdgeNgramField(model_attr='name')

    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()