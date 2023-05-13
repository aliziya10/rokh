from django.contrib import admin
from django.urls import path, re_path,include
from .views import *


app_name="home"

urlpatterns = [

    path('home/',page_home),
    path('admins/',admin_list),
    # path('forms/<int:pk>/',form_list),
    # re_path('menus/(?P<pk>[0-9])?/', menu_list),
    path('menus/<int:pk>/',menu_list),
    path('slides/<int:pk>/',slide_list),
    path('tickets/<int:pk>/', tickets_list),
    path('mainsettings/',mainsettings),
    # path('forms/',form_list),
    path('menus/',menu_list),
    path('slides/',slide_list),
    path('tickets/', tickets_list),
    path('posts/<int:pk>/', posts_list, name='posts_list2'),
    path('posts/', posts_list, name='posts_list'),
    path('teammates/<int:pk>/', teammate_list),
    path('teammates/', teammate_list),
    # path('otps/', seeredis),

]




