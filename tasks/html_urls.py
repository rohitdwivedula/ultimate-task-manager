
from django.urls import path   
import tasks.html_views as html_views
  
urlpatterns = [
	path('login/', html_views.login_view),
	path('forgot/', html_views.forgot_pwd_view),
	path('sign-up/', html_views.sign_up_view),
	path('taskboard/', html_views.taskboard_view),
]