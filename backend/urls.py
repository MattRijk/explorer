from django.conf.urls import url, include
from backend.views import index, edit_user, delete_user
from pins.views import  create_category, edit_category, delete_category

urlpatterns = [

    url(r'^$', view=index, name='index'),
    # create view
    url(r'^user/edit/(?P<pk>\d+)$', view=edit_user, name='editUser'),
    url(r'^user/delete/(?P<pk>\d+)$', view=delete_user, name='deleteUser'),

    url(r'^categories/create/', view=create_category, name='createCategory'),
    url(r'^categories/edit/(?P<slug>[\w-]+)/$', view=edit_category, name='editCategory'),
    url(r'^categories/delete/(?P<slug>[\w-]+)/$', view=delete_category, name='deleteCategory'),
]