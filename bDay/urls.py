from django.conf.urls import url

from . import views

app_name = 'bDay'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth$', views.save_tokens)
]