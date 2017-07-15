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
    url(r'^experiments/(?P<e_pk>\d+)/evacs$',
        views.vac_list, name='vac_list'),
    url(r'^experiments/(?P<e_pk>\d+)/evacs/new$',
        views.vac_create, name='vac_new'),
    url(r'^experiments/(?P<e_pk>\d+)/evacs/edit/(?P<pk>\d+)$',
        views.vac_update, name='vac_edit'),
    url(r'^experiments/(?P<e_pk>\d+)/evacs/delete/(?P<pk>\d+)$',
        views.vac_delete, name='vac_delete'),
    url(r'^assignments/(?P<a_pk>\d+)/evacs/(?P<v_pk>\d+)/evaluation/new$',
        views.evaluation_update, name='evaluation_edit'),
]
