from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import ContactUs, Feedback, Notification, Setup, StaffProfile, Transaction, User, UserProfile, Wallet


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True

class UserFeedbackInline(admin.ModelAdmin):
    model = Feedback
    can_delete = True
    list_display = ('mobile', 'text', 'rate', 'user')

class UserContactInline(admin.ModelAdmin):
    model = ContactUs
    can_delete = True
    list_display = ('contact', 'mobile')

class SetupInline(admin.ModelAdmin):
    model = Setup
    can_delete = True
    list_display = ('name', 'longitude', 'latitude', 'isOccupied', 'zip')

class NotificationInline(admin.ModelAdmin):
    model = Notification
    can_delete = True
    list_display = ('id', 'text', 'isRead', 'setup', 'user')

class TransactionInline(admin.ModelAdmin):
    model = Transaction
    can_delete = True
    list_display = ('transaction_id', 'money', 'user', 'setup')

class WalletInline(admin.ModelAdmin):
    model = Wallet
    can_delete = True
    list_display = ('user', 'balance', 'createdAt', 'updatedAt')

class StaffInline(admin.ModelAdmin):
    model = StaffProfile
    can_delete = True
    list_display = ('name', 'mobile','setup')

admin.site.register(StaffProfile, StaffInline)
admin.site.register(Wallet, WalletInline)
admin.site.register(Transaction, TransactionInline)
admin.site.register(Notification, NotificationInline)
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
