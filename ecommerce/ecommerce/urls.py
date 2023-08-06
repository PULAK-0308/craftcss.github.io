"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from craft.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('register',register,name='register'),
    path('loginuser',loginuser,name='loginuser'),
    path('logoutuser',logoutuser,name='logoutuser'),
    path('mainpage',mainpage,name='mainpage'),
    path('dreamcatchers',dreamcatchers,name='dreamcatchers'),
    #path('resinproducts',resinproducts,name='resinproducts'),
    path('gallery',gallery,name='gallery'),
     path('checkout', checkout, name="Checkout"),
    path('handlerequest', handlerequest, name="HandleRequest"),
    
    
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

