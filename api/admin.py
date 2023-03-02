from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import AdminNotification, ContactUs, Feedback, InOutCount, Notification, Setup, SetupTransactionSuccess, StaffProfile, Transaction, User, UserProfile, Wallet, WalletTransaction


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = True

class UserFeedbackInline(admin.ModelAdmin):
    model = Feedback
    can_delete = True
    list_display = ('mobile', 'text', 'rate', 'user','createdAt','updatedAt')

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
    list_display = ('id','text','isRead','setup','user','createdAt','updatedAt')

class AdminNotificationInline(admin.ModelAdmin):
    model = AdminNotification
    can_delete = True
    list_display = ('id','text','isRead','setup','user','createdAt','updatedAt')

class TransactionInline(admin.ModelAdmin):
    model = Transaction
    can_delete = True
    list_display = ('transaction_id', 'money', 'user', 'setup','w_id')

class WalletInline(admin.ModelAdmin):
    model = Wallet
    can_delete = True
    list_display = ('user', 'balance', 'createdAt', 'updatedAt')

class StaffInline(admin.ModelAdmin):
    model = StaffProfile
    can_delete = True
    list_display = ('name', 'mobile','setup')

class InOutCountInline(admin.ModelAdmin):
    model = InOutCount
    can_delete = True
    list_display = ('inSetup', 'outSetup','setup','createdAt','updatedAt')

class WalletTransactionInline(admin.ModelAdmin):
    model = WalletTransaction
    can_delete = True
    list_display = ('transaction_id', 'mobile', 'wallet_id', 'amount','createdAt','updatedAt')

admin.site.register(WalletTransaction, WalletTransactionInline)
admin.site.register(InOutCount, InOutCountInline)
admin.site.register(StaffProfile, StaffInline)
admin.site.register(Wallet, WalletInline)
admin.site.register(Transaction, TransactionInline)
admin.site.register(Notification, NotificationInline)
admin.site.register(AdminNotification, AdminNotificationInline)
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
