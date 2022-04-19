from django.urls import path
from django.http import HttpResponse
from db_manage import views
urlpatterns = [
    path("select/", views.searchRes),
    path("adjust/", views.adjustReq),
]
