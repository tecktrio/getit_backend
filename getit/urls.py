"""getit URL Configuration

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
from getit_api import views as user_side
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('search',user_side.Search.as_view()),
    path('Signup',user_side.Sign_up.as_view()),
    path('Login',user_side.Login.as_view()),
    path('Logout',user_side.Logout.as_view()),
    path('HomePage',user_side.HomePage.as_view()),
    path('Product/<str:keyword>',user_side.Product_Handling.as_view()),
    path('Product',user_side.Product_Handling.as_view()),
    path('howtouse',user_side.HowToUse.as_view()),
    path('live',user_side.Live.as_view()),
    path('settings',user_side.settings.as_view()),


]
