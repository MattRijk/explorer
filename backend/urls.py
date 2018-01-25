from django.conf.urls import url, include
from backend.views import index, edit_user, delete_user, edit_category, delete_category

urlpatterns = [
    url(r'^$', view=index, name='index'),
    url(r'^user/edit/(?P<pk>\d+)$', view=edit_user, name='editUser'),
    url(r'^user/delete/(?P<pk>\d+)$', view=delete_user, name='deleteUser'),
    url(r'^category/edit/(?P<slug>[\w-]+)/$', view=edit_category, name='editCategory'),
    url(r'^category/delete/(?P<slug>[\w-]+)/$', view=delete_category, name='deleteCategory'),
]