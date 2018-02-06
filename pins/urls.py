from django.conf.urls import url, include
from pins.views import pin_detail

urlpatterns = [
    url(r'^(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', pin_detail, name='pin_detail'),
]

