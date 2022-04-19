"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from util import get_csrf_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/666', view=lambda e: HttpResponse('戏说不是胡说')),
    path('api/db_manage/', include("db_manage.urls")),
    path('api/db_admin/', include("db_admin.urls")),
    path('api/blockchain_manage/', include("blockchain_manage.urls")),
    path('api/connect', view=get_csrf_token)
]
