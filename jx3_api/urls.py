"""jx3_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
xadmin.autodiscover()
# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.urls import path, re_path, include

from django.conf import settings
from django.views.static import serve
from home import views

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('user/', include('user.urls')),
    path('article/', include('article.urls')),
    path('player/',include('player.urls')),
    path('', include('home.urls')),  # 首页主路由
    path('search/', include('haystack.urls')),


    re_path(r'.+',views.ErrorView.as_view()),
]
