from django.conf.urls import include, url
from .views import EventListView, EventDetailView


urlpatterns = [
    url(r'$', EventListView.as_view(), name='events_list'),
    url(r'event/(?P<pk>\d+)/$', EventDetailView.as_view(), name='event_detail'),
]
