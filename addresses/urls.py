from django.urls import path

from addresses.views import addresses

urlpatterns =[ 
    path("get_adress/", ),
    path("post_adress/", ),
    path("update_adress/",),
    path("delet_adress/",)]