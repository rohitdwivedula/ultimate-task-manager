from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from authentication.helper import UserHelper
from authentication.conf import JWT_COOKIE_KEY

from django.http import HttpResponse
from django.views.generic import View

class AllTasks(APIView):
	pass

class OneTask(APIView):
	pass
