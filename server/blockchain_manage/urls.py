from django.urls import path
from django.http import HttpResponse
from blockchain_manage import views
urlpatterns = [
    #path("SRT_Create/", views.SRT_Create),
    path("get_SRT/", views.get_SRT),
    path("get_School/", views.get_School),
    path("get_Ret/", views.get_ret),
    #path("Course_Create/", views.Course_Create)
]
