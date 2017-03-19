from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^index/', views.index,name='index'),
    url(r'^$', views.index,name='index'),
    url(r'^archive/$', views.archive,name='archive'),
    url(r'^article/$', views.article,name='article'),
    url(r'^test/$', views.test,name='test'),
]
