from Explorer import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from pins.views import home_page, category_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^pins/', include('pins.urls', namespace='pins')),
    url(r'^$', view=home_page, name='home_page'),
    url(r'^backend/', include('backend.urls', namespace='backend')),
    url(r'^', include('pins.urls', namespace='pins')),
    url(r'^categories/$', view=category_list, name='category_list'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
