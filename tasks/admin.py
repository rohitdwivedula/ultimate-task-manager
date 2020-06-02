from django.contrib import admin
from tasks.models import Label, Task, SubTask


class TaskAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'due_on', 'status', 'priority')
	list_filter = ('labels',)

class SubTaskAdmin(admin.ModelAdmin):
	list_display = ('name', 'status')
	list_filter = ('task',)

class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)

admin.site.register(Label, LabelAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(Task, TaskAdmin)
