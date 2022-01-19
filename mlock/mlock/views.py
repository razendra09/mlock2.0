from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import requests

# Homepage Functions
def index(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'auth/login.html')
def logout(request):
    return render(request, 'auth/logout.html')

# Dashboard Functions

def profile(request):
    return render(request, 'auth/profile.html')
def exchangesetup(request):
    return render(request, 'auth/exchangesetup.html')

# stockbot Functions
def createnewbot(request):
    return render(request, 'bots/createnewbot.html')
def allbots(request):
    return render(request, 'bots/allbots.html')
def allbottasks(request):
    return render(request, 'bots/allbottasks.html')
def managebot(request):
    return render(request, 'bots/managebot.html')

# Bot script test Functions

def runstockbot(requests):
    return render(request, 'bots/scripttest.html')



# cryptobot Functions

def addnewdeal(request):
    return render(request, 'cryptobot/addnewdeal.html')
def allcryptodeals(request):
    return render(request, 'cryptobot/alldeals.html')
def addnewcryptorule(request):
    return render(request, 'cryptobot/addnewrule.html')
def allcryptorules(request):
    return render(request, 'cryptobot/allrules.html')

# Utilities
def cryptocalculator(request):
    return render(request, 'calculators/cryptocalculator.html')

