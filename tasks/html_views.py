from django.views.generic import View
from django.shortcuts import render

def index_view(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def forgot_pwd_view(request):
    return render(request, "forgotpw.html")

def reset_pwd_view(request):
    return render(request, "resetpw.html")

def sign_up_view(request):
    return render(request, "signup.html")

def taskboard_view(request):
	return render(request, "taskboard.html")

def profile_view(request):
	return render(request, "profile.html")

def editprofile_view(request):
	return render(request, "editprofile.html")

def signout_view(request):
    return render(request, "signout.html")

def labels_view(request):
    return render(request, "labels.html")
