from django.conf.urls import url
from pins.views import pin_detail, category_detail, all_images, pin_image

urlpatterns = [
    url(r'^images/$', all_images, name='all_images'),
    url(r'^image/(?P<slug>[\w-]+)/$', pin_image, name='pin_image'),
    url(r'^(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', pin_detail, name='pin_detail'),
    url(r'^(?P<slug>[\w-]+)/$', category_detail, name='category_detail'),
]

