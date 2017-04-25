import datetime
from haystack import indexes
from .models import *

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    #content_auto = indexes.EdgeNgramField(model_attr='product.name')

    # suggestions = indexes.FacetCharField()

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()