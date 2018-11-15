from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(?P<word>[\w-]+)/$', views.search, name='search'),
    url(r'^$', views.index, name='index'),
]




MOVE EVERYTHING TO ADMIN ITSELF IF URLS HAVE NO ISSUES