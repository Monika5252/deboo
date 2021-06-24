from api.admin_views.adminviews import AdminFeedbackApiView, AdminInOutCountApiView, AdminNotificationApiView, AdminSetupApiView, AdminTransactionsApiView, AdminUserApiView, InOutDetailsApiView, AdminStaffApiView
from django.conf.urls import url, include
from rest_framework import routers
from api.views import AllTransactionApiView, StaffDetailsApiView, ContactApiView, ContactUsApiView, FeedbackApiView, FeedbackDetailsApiView, GetStaffApiView, NearMeApiView, NotificationApiView, NotificationDetailsApiView, OccupySetupView, SetupApiView, SetupDetailsApiView, TransactionDetailsApiView, TransactionsApiView, UserViewSet, WalletApiView, WalletDetailsApiView
from django.urls import path, include
from . import views
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^feedback/', FeedbackApiView.as_view()),
    path('feedbackdetail/<int:feed_id>/', FeedbackDetailsApiView.as_view()),

    url(r'^contact/', ContactApiView.as_view()),
    path('contactdetail/<int:contact_id>/', ContactUsApiView.as_view()),

    url(r'^setup/', SetupApiView.as_view()),
    path('setupdetail/<int:setup_id>/', SetupDetailsApiView.as_view()),

    path('occupy/<int:setup_id>/', OccupySetupView.as_view()),
    
    url(r'^notifications/', NotificationApiView.as_view()),
    path('notificationdetails/<int:notify_id>/', NotificationDetailsApiView.as_view()),

    url(r'^transaction/', TransactionsApiView.as_view()),
    # url(r'^allTransaction/', AllTransactionApiView.as_view()),
    path('transactiondetails/<int:transaction_id>/', TransactionDetailsApiView.as_view()),

    url(r'^staff/', GetStaffApiView.as_view()),
    path('staffdetail/<int:staff_id>/', StaffDetailsApiView.as_view()),

    url(r'^nearme/', NearMeApiView.as_view()),

    url(r'^wallet/', WalletApiView.as_view()),
    path('walletmoney/<int:wallet_id>/', WalletDetailsApiView.as_view()),

    url(r'^login/', views.login_view, name="login_view"),
    url(r'^refresh_token/', views.refresh_token_view, name="refresh_token"),

    url(r'^inout/', AdminInOutCountApiView.as_view()),
    path('inOutdetails/<int:inOut_id>/', InOutDetailsApiView.as_view()),

    url(r'^allnotification/', AdminNotificationApiView.as_view()),
    url(r'^allsetup/', AdminSetupApiView.as_view()),
    url(r'^alltransaction/', AdminTransactionsApiView.as_view()),
    url(r'^allfeedback/', AdminFeedbackApiView.as_view()),
    url(r'^allusers/', AdminUserApiView.as_view()),
    url(r'^allstaff/', AdminStaffApiView.as_view())

]