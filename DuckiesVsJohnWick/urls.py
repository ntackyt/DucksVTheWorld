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
    path('login/', views.login, name='login'), 
    path('postlogin/', views.postlogin, name='postlogin'),
    path('signup/', views.signup, name='signup'),
    path('postsignup/', views.postsignup, name='postsignup'),
    path('add_pin/', views.add_pin, name='add_pin'),
    #path('logout/', LogoutView.as_view(next_page=''), name='logout'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('admin/', admin.site.urls),
]