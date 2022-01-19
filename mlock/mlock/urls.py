from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [

    path('admin/', admin.site.urls),


# Auth  & Profile URLs
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('exchangesetup', views.exchangesetup, name='exchangesetup'),

# stock Bot URLS
    path('createnewbot', views.createnewbot, name='createnewbot'),
    path('allbots', views.allbots, name='allbots'),
    path('allbottasks', views.allbottasks, name='allbottasks'),
    path('managebot', views.allbottasks, name='managebot'),

# Crypto Bot URLS
    path('addnewdeal', views.addnewdeal, name='addnewdeal'),
    path('allcryptodeals', views.allcryptodeals, name='allcryptodeals'),
    path('addnewcryptorule', views.addnewcryptorule, name='addnewcryptorule'),
    path('allcryptorules', views.allcryptorules, name='allcryptorules'),

# Utilities
    path('cryptocalculator', views.cryptocalculator, name='cryptocalculator'),
]