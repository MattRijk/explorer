from django.conf.urls import url
from backend.views import index, create_user, edit_user, delete_user
from pins.views import  admin_category_list, create_category, edit_category, delete_category
from pins.views import create_pin, edit_pin, delete_pin, pins_list, DataFormView


urlpatterns = [
    url(r'^$', view=index, name='index'),
    url(r'^user/create/', view=create_user, name='createUser'),
    url(r'^user/edit/(?P<pk>\d+)$', view=edit_user, name='editUser'),
    url(r'^user/delete/(?P<pk>\d+)$', view=delete_user, name='deleteUser'),

    url(r'^categories/$', view=admin_category_list, name='admin_category_list'),
    url(r'^categories/create/', view=create_category, name='createCategory'),
    url(r'^categories/edit/(?P<slug>[\w-]+)/$', view=edit_category, name='editCategory'),
    url(r'^categories/delete/(?P<slug>[\w-]+)/$', view=delete_category, name='deleteCategory'),

    url(r'^pins/$', view=pins_list, name='pins_list'),

    url(r'^pins/create/', view=create_pin, name='createPin'),
    url(r'^pins/edit/(?P<slug>.+)/$', view=edit_pin, name='editPins'),
    url(r'^pins/delete/(?P<slug>.+)/$', view=delete_pin, name='deletePins'),

    url(r'^csv-upload/$', DataFormView.as_view(), name='csv_upload'),

]