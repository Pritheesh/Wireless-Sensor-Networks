from django.conf.urls import url

from Graph import views

urlpatterns = [
    url(r'^$', views.form_view),
    # url(r'^api/register/$', api_views.register, name='api-register'),
]