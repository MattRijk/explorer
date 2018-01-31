from django.conf.urls import url
from backend.views import index, create_user, edit_user, delete_user
from pins.views import create_category, edit_category, delete_category, category_list
from pins.views import create_pin, edit_pin, pins_list


urlpatterns = [
    url(r'^$', view=index, name='index'),
    url(r'^user/create/', view=create_user, name='createUser'),
    url(r'^user/edit/(?P<pk>\d+)$', view=edit_user, name='editUser'),
    url(r'^user/delete/(?P<pk>\d+)$', view=delete_user, name='deleteUser'),

    url(r'^categories/$', view=category_list, name='categories'),
    url(r'^categories/create/', view=create_category, name='createCategory'),
    url(r'^categories/edit/(?P<slug>[\w-]+)/$', view=edit_category, name='editCategory'),
    url(r'^categories/delete/(?P<slug>[\w-]+)/$', view=delete_category, name='deleteCategory'),

    url(r'^pins/$', view=pins_list, name='pins_list'),
    url(r'^pins/create/', view=create_pin, name='createPin'),
    url(r'^pins/edit/(?P<slug>[\w-]+)/$', view=edit_pin, name='editPins'),

]