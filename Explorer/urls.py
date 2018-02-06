from Explorer import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from pins.views import home_page

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', view=home_page, name='home_page'),
    url(r'^backend/', include('backend.urls', namespace='backend')),
    url(r'^', include('pins.urls', namespace='pins')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
