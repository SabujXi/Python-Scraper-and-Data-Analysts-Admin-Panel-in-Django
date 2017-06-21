from django.conf.urls import url, include
from data.views import index, DataFormView

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^data_form/(?P<data_unique_id>[0-9a-zA-Z]*)$', index, name="data_form")
]

