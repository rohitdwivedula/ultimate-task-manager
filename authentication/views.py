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
from django.shortcuts import render
from django.views.generic import View
import pyotp

class SignupView(APIView):
    """View class for signing up to the service"""
    def post(self, request):
        payload = request.data
        try:
            email = payload['email'].strip().lower()
            password = payload['password']
            first_name = payload['first_name']
            last_name = payload['last_name']

            ip_address = request.META['REMOTE_ADDR']

            if UserHelper.check_user_exists(email):
                message = {'error': 'Email ID already in use'}
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

            local_vars = locals()
            kwargs = {}
            for x in ('first_name', 'last_name', 'ip_address'):
                kwargs[x] = locals()[x]

            user = UserHelper.create_user(email, password, **kwargs)


            user.is_verified = False  # all accounts are active at signup, use admin panel to deactivate
            UserHelper.set_new_activation_token(user, force_set=True)
            user.save()

            UserHelper.send_activation_email(user, request)
            UserHelper.user_onboarding(user, request)
            message = {'success': "User Creation Successful. Verify email."}
            return Response(message, status=status.HTTP_200_OK)
        except (KeyError):
            message = {'error': "Invalid schema"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """View class to login to the service"""
    def post(self, request):
        payload = request.data
        try:
            email = payload['email'].strip().lower()
            password = payload['password']

            user = UserHelper.check_user_exists(email)
            if not user:
                message = {'error': "Account not found"}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            if not user.is_verified:
                if UserHelper.set_new_activation_token(user, save_user=True):
                    UserHelper.send_activation_email(user, request)
                message = {'error': "Email not verified. Verify email and try again."}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            if not UserHelper.check_user_credentials(user, password):
                message = {'error': "Invalid email or password"}
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            if user.two_factor_enabled:
                if "otp" not in payload:
                    message = {'error': "User has 2FA enabled. otp not found or is invalid."}
                    return Response(message, status=status.HTTP_403_FORBIDDEN)
                otp_sent = payload['otp']
                totp = pyotp.TOTP(user.two_factor_secret)
                if not totp.verify(otp_sent):
                    print(totp.now())
                    message = {'error': "User has 2FA enabled. otp not found or is invalid."}
                    return Response(message, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            message = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

            response = Response(message, status=status.HTTP_200_OK)
            response.set_cookie(JWT_COOKIE_KEY, access_token, max_age=None, secure=True, httponly=True,
                                samesite='strict')
            return response
        except (KeyError):
            message = {'error': "Invalid schema"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserInformationView(APIView):
    """View class to view user information"""
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """Return user's information"""
        user = request.user
        message = {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'date_joined': user.date_joined,
            'email_notifications_enabled': user.email_notifications_enabled,
            'discord_notifications_enabled': user.discord_notifications_enabled,
            'discord_webhook_url': user.discord_webhook_url,
            'remind_duration': user.remind_duration,
            'two_factor_enabled': user.two_factor_enabled
        }
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request):
        """Update the user's information"""
        user = request.user
        payload = request.data

        keys = ('first_name', 'last_name', 'bio')
        if 'first_name' in payload:
        	user.first_name = payload['first_name']
        if 'last_name' in payload:
        	user.last_name = payload['last_name']
        if 'bio' in payload:
        	user.bio = payload['bio']
        if 'email_notifications_enabled' in payload:
        	user.email_notifications_enabled = payload['email_notifications_enabled']
        if 'discord_notifications_enabled' in payload:
        	user.discord_notifications_enabled = payload['discord_notifications_enabled']
        if 'discord_webhook_url' in payload:
        	user.discord_webhook_url = payload['discord_webhook_url']
        if 'remind_duration' in payload:
        	user.remind_duration = payload['remind_duration']

        user.save()

        message = {'success': "Successfully updated user information"}
        return Response(message, status=status.HTTP_200_OK)

class ChangeCredentialsView(APIView):
    """View class to change user credentials"""
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """Change the user credentials"""
        user = request.user
        payload = request.data
        password = payload['password']

        if not password:
            message = {'error': 'New password is invalid'}
            return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        UserHelper.update_user_password(user, password)

        message = {'success': "Successfully updated user credentials"}
        return Response(message, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """View class to reset user credentials"""
    def get(self, request):
        payload = request.GET

        try:
            email = payload['email'].strip().lower()
            user = User.objects.filter(email=email)

            if not user:
                # claim that the email has been sent
                message = {'success': "Email sent, if associated account exists111"}
                return Response(message, status=status.HTTP_200_OK)

            user = user[0]

            if not user.is_verified:
                # Send verification email
                if UserHelper.set_new_activation_token(user, save_user=True):
                    UserHelper.send_activation_email(user, request)
                message = {'error': "Email not verified. Please verify email before attempting password reset"}
                return Response(message, status=status.HTTP_403_FORBIDDEN)

            timediff = (timezone.now() - user.generated_at).total_seconds()
            if timediff <= 300:
                # maximum of one email every 5 minutes
                message = {'error': "Email was sent in the last 5 minutes"}
                response = Response(message, status=status.HTTP_429_TOO_MANY_REQUESTS)
                response['Retry-After'] = 300 - timediff
                return response
            else:
                if UserHelper.set_new_forgot_password_token(user, save_user=True):
                    # split the otp into two 4-digit halves
                    verification_token_str = str(user.verification_token)
                    message = "Your OTP for password reset is " + verification_token_str + " \n\n Please do not share with anyone. Best."
                    user.email_user("UltimateTaskManager - Forgot Password", message)
            message = {'success': 'Email with OTP sent, if associated account exists222'}
            return Response(message, status=status.HTTP_200_OK)
        except KeyError:
            message = {'error': 'Invalid schema'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        payload = request.data
        try:
            email = payload['email'].strip().lower()
            password = payload['password']
            otp = payload['otp']

            user = User.objects.filter(email=email)
            if not user:
                message = {'error': 'Invalid Email ID or OTP'}
                return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = user[0]
            if not user.is_verified:
                message = {'error': 'Invalid Email ID or OTP'}
                return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # remove any spaces in the otp
            otp = otp.replace(" ", "")
            if not user.verification_token == otp:
                message = {'error': "Invalid Email ID or OTP"}
                return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            timediff = (timezone.now() - user.generated_at).total_seconds()
            if timediff > 900:
                # otp invalid after 15 minutes
                message = {'error': "OTP expired. Try again."}
                return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # generate a new token so that the old one can't be used to reset
            # password again
            user.verification_token = UserHelper.generate_token(8)
            UserHelper.update_user_password(user, password)
            user.save()

            message = "Your password has been reset successfully."
            user.email_user("UltimateTaskManager - Password Reset Successful",message)
            message = {'success': "Password reset successful"}
            return Response(message, status=status.HTTP_200_OK)
        except KeyError:
            message = {'error': 'Invalid schema'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

def verify_view(request):
    payload = request.GET
    try:
        email = payload['email']
        token = payload['token']
        if not token:
            return render(request, "verified.html", {'message':"Invalid email or token", 'verified': False})

        user = User.objects.filter(email=email)
        if not user:
            return render(request, "verified.html", {'message':"Invalid email or token", 'verified':False})
        user = user[0]

        if user.is_verified:
        	return render(request, "verified.html", {'message':"Your email has already been verified before.", 'verified':False})

        timediff = (timezone.now() - user.generated_at).total_seconds()
        if timediff > 86400:
            # verification timed out, delete their old token
            # and generate new token and email it to them
            user.verification_token = UserHelper.generate_token(64)
            user.generated_at = timezone.now()
            user.save()

            UserHelper.send_activation_email(user, request)
            return render(request, "verified.html", {'message':"Your email was NOT verified because the link expired. \
            	A new link has been emailed to you", 'verified':False})
        if not user.verification_token == token:
            return render(request, "verified.html", {'message':"Your email was NOT verified - invalid token or email id", 'verified':False})
        user.is_verified = True
        # invaldidate the the verification_token
        user.verification_token = UserHelper.generate_token(8)
        user.save()
        return render(request, "verified.html", {'message':"Your account has been activated. Happy planning!", 'verified':True})
    except (KeyError):
    	return render(request, "verified.html", {'message':"Your account has not been activated. Something went wrong.", 'verified':False})


class TwoFactorView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        user = request.user
        user.two_factor_enabled = True
        user.two_factor_secret = pyotp.random_base32()
        user.save()
        message = {
            'message': '2FA enabled.',
            'secret': user.two_factor_secret,
            'uri': pyotp.totp.TOTP(user.two_factor_secret).provisioning_uri(user.email, issuer_name="Ultimate Task Manager")
        }
        return Response(message, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user.two_factor_enabled = False
        user.save()
        message = {
            'message': '2FA disabled successfully'
        }
        return Response(message, status=status.HTTP_200_OK)
