
from django.urls import path
import tasks.html_views as html_views

urlpatterns = [
	path('login/', html_views.login_view),
	path('forgot/', html_views.forgot_pwd_view),
	path('reset/', html_views.reset_pwd_view),
	path('sign-up/', html_views.sign_up_view),
	path('taskboard/', html_views.taskboard_view),
    path('profile/', html_views.profile_view),
	path('editprofile/', html_views.editprofile_view),
	path('signout/', html_views.signout_view),
	path('labels/', html_views.labels_view),
	path('', html_views.index_view)

]
