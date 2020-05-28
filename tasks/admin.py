from django.contrib import admin
from tasks.models import Label, Task, SubTask

admin.site.register(Task)
admin.site.register(SubTask)


class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)

admin.site.register(Label, LabelAdmin)
