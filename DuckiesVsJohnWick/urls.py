"""
Definition of urls for DuckiesVsJohnWick.
"""
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms
from app import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('map/', views.map, name='map'),
    path('game/', views.game, name='game'),
    path('login/', views.login, name='login'), 
    path('postlogin/', views.postlogin, name='postlogin'),
    path('signup/', views.signup, name='signup'),
    path('postsignup/', views.postsignup, name='postsignup'),
    path('add_pin/', views.add_pin, name='add_pin'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('whatwedo/', views.whatwedo, name='whatwedo'),
    path('show_user_profile/<str:user_id>/', views.show_user_profile, name='show_user_profile'),
    
    path('admin/', admin.site.urls),
]