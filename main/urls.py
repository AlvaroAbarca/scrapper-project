"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core.views import (config_view, index, index_landing, login_view,
                        product_detail, register_view, updates_view, unfollow_product,
                        search_product)
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('product_detail/<int:pk>/', product_detail, name="product_detail"),
    path('config/', config_view, name="config_view"),
    path('updates/', updates_view, name="updates_view"),
    path('unfollow/<int:pk>/', unfollow_product, name="unfollow_product"),
    path('search_product/', search_product, name="search_product"),
    path('', index_landing, name="index_landing"),
]
