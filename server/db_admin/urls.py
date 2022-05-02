from django.urls import path
from django.http import HttpResponse
from db_admin import views
urlpatterns = [
    path("adjust/", views.adjustReq),
    path("select/", views.searchReq)
]
