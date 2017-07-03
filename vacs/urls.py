from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^experiments/(?P<pk>\d+)/$',
        views.ExperimentDetailView.as_view(), name='experiment-detail'),
    url(r'^experiments/$',
        views.ExperimentListView.as_view(), name='experiment-list'),
    url(r'^experiments/new$',
        views.ExperimentCreateView.as_view(), name='experiment-new'),
    url(r'^experiments/edit/(?P<pk>\d+)$',
        views.ExperimentUpdateView.as_view(), name='experiment-edit'),
    url(r'^experiments/delete/(?P<pk>\d+)$',
        views.ExperimentDeleteView.as_view(), name='experiment-delete'),
]
