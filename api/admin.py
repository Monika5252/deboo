from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import ContactUs, Feedback, Setup, User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True

class UserFeedbackInline(admin.ModelAdmin):
    model = Feedback
    can_delete = True

class UserContactInline(admin.ModelAdmin):
    model = ContactUs
    can_delete = True

class SetupInline(admin.ModelAdmin):
    model = Setup
    can_delete = True
    list_display = ('name', 'longitude', 'latitude', 'isOccupied', 'zip')

admin.site.register(Feedback, UserFeedbackInline)
admin.site.register(ContactUs, UserContactInline)
admin.site.register(Setup, SetupInline)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('mobile', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('mobile', 'email' 'first_name', 'last_name')
    ordering = ('mobile',)
    inlines = (UserProfileInline, )
