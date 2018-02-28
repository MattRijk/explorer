import datetime
from haystack import indexes
from pins.models import Pin, Category

class PinIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    published = indexes.DateTimeField(model_attr='published')

    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Pin

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
