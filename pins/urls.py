from django.conf.urls import url, include
from pins.views import pin_detail

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', view=pin_detail, name='pin_detail'),
]