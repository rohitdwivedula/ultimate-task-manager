from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authentication.forms import UserChangeForm, UserCreationForm
from authentication.models import User


class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    """
    Instance variables:
    * list_display -- refer django.contrib.admin.ModelAdmin.list_display
    * list_filter -- refer django.contrib.admin.ModelAdmin.list_filter
    * fieldsets -- refer django.contrib.admin.ModelAdmin.fieldsets
    * add_fieldsets -- the fields used when creating a new user
    * search_fields -- refer django.contrib.admin.ModelAdmin.search_fields
    * ordering -- refer django.contrib.admin.ModelAdmin.ordering
    * filter_horizontal -- refer django.contrib.admin.ModelAdmin.filter_horizontal
    """

    list_display = ('email', 'first_name', 'last_name')
    list_filter = ()
    fieldsets = (
        ('Basic Information', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Groups', {'fields': ('groups', )}),
        ('Permissions', {'fields': ('is_superuser',)}),
        ('Security Info', {'fields': ('date_joined', 'ip_address', 'generated_at', 'verification_token', 'is_verified')}),
        ('Settings',{'fields': ('email_notifications_enabled', 'discord_notifications_enabled', 'discord_webhook_url', 'remind_duration')})
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'bio', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
