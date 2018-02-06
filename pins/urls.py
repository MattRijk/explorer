from django.conf.urls import url
from pins.views import pin_detail, category_detail

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', category_detail, name='category_detail'),
    url(r'^(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', pin_detail, name='pin_detail'),
]

