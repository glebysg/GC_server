from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^experiments/$',
        views.experiment_list, name='experiment_list'),
    url(r'^experiments/new$',
        views.experiment_create, name='experiment_new'),
    url(r'^experiments/edit/(?P<pk>\d+)$',
        views.experiment_update, name='experiment_edit'),
    url(r'^delete/(?P<pk>\d+)$',
        views.experiment_delete, name='experiment_delete'),
]
