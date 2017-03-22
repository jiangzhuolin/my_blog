from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^index/', views.index,name='index'),
    url(r'^$', views.index,name='index'),
    url(r'^archive/$', views.archive,name='archive'),
    url(r'^article/$', views.article,name='article'),
    url(r'^login/$', views.do_login,name='login'),
    url(r'^reg/$', views.do_reg,name='reg'),
    url(r'^logout/$', views.do_logout,name='logout'),
    url(r'^comment_post$', views.comment_post,name='comment_post'),
    url(r'^test', views.test,name='test'),
]
