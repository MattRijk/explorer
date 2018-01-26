from django.conf.urls import url, include
from django.contrib import admin
from pins.views import homepage

urlpatterns = [
    url(r'^', include('allauth.urls')),

    url(r'^$', view=homepage, name='homepage'),
    url(r'^backend/', include('backend.urls', namespace='backend')),

    url(r'^admin/', admin.site.urls),
]
