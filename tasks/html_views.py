from django.views.generic import View
from django.shortcuts import render

def login_view(request):
    return render(request, "login.html")

def forgot_pwd_view(request):
    return render(request, "forgotpw.html")

def sign_up_view(request):
    return render(request, "signup.html")

def taskboard_view(request):
	return render(request, "taskboard.html")

def profile_view(request):
	return render(request, "profile.html")

def editprofile_view(request):
	return render(request, "editprofile.html")
