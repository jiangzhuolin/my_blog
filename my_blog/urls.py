"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from blog.upload import upload_image

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^uploads/(?P<path>.*)$", \
                # 使用Django自带的方法处理路径中带有uploads的请求的静态文件的方法，
                "django.views.static.serve", \
                # 配置的绝对路径
                {"document_root": settings.MEDIA_ROOT,}),

    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    url(r'^',include('blog.urls'))
]
