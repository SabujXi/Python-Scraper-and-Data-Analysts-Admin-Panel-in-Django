from django.conf.urls import url, include
from data.views import index, DataFormView, delete_data, list_data, list_city_found, list_city_not_found

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^data_form/(?P<data_id>[0-9a-zA-Z]*)$', DataFormView.as_view(), name="data_form"),
    url(r'^data_list/(?P<city>.+)$', list_data, name="list_data"),
    url(r'^data_delete/(?P<data_id>[0-9a-zA-Z]+)$', delete_data, name="delete_data"),
    url(r'^list_city$', list_city_found, name="list_city"),
    url(r'^list_city_not_found$', list_city_not_found, name="list_city_not_found"),

]

