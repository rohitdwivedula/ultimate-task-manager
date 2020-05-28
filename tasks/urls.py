from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import tasks.views as api_views

urlpatterns = [
    path('tasks/', api_views.AllTasks.as_view()),
	path('task/', api_views.OneTask.as_view())    
]

urlpatterns = format_suffix_patterns(urlpatterns)