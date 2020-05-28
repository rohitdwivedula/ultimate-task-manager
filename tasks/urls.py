from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import tasks.views as api_views

urlpatterns = [
	# GET all tasks or create (POST) a task
	path('tasks/', api_views.AllTasksView.as_view()),
	
	# GET a task, update (POST) a task, DELETE a task
	path('tasks/<uuid:task_uuid>/', api_views.TaskView.as_view()),

	# GEL all labels or create (POST) a label
	path('labels/', api_views.AllLabelsView.as_view()),

	# manage a label - GET to retrieve info, POST to update, DELETE to remove
	path('labels/<uuid:label_uuid>/', api_views.LabelView.as_view()),

	# GET all subtasks of a task or POST (create) a subtask
	path('tasks/<uuid:task_uuid>/subtask/', api_views.AllSubTaskView.as_view()),

	# manage a subtask - GET to retrieve info, POST to update, DELETE to remove
	path('subtasks/<uuid:subtask_uuid>/', api_views.SubTaskView.as_view()),
]

# TODO: Add and remove labels from a task

urlpatterns = format_suffix_patterns(urlpatterns)