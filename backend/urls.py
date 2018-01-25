from django.conf.urls import url, include
from backend.views import index, edit_user, delete_user

urlpatterns = [
    url(r'^$', view=index, name='index'),
    url(r'^edit/(?P<pk>\d+)$', view=edit_user, name='edit'),
    url(r'^delete/(?P<pk>\d+)$', view=delete_user, name='delete'),
]