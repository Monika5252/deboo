from django.conf.urls import url, include
from rest_framework import routers
from api.views import AllTransactionApiView, ContactApiView, ContactUsApiView, FeedbackApiView, FeedbackDetailsApiView, GetStaffApiView, NearMeApiView, NotificationApiView, NotificationDetailsApiView, OccupySetupView, SetupApiView, SetupDetailsApiView, TransactionsApiView, UserViewSet, WalletApiView, WalletDetailsApiView
from django.urls import path, include

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
    path('notifications/<int:notify_id>/', NotificationDetailsApiView.as_view()),

    url(r'^transaction/', TransactionsApiView.as_view()),
    url(r'^allTransaction/', AllTransactionApiView.as_view()),

    url(r'^staff/', GetStaffApiView.as_view()),

    url(r'^nearme/', NearMeApiView.as_view()),

    url(r'^wallet/', WalletApiView.as_view()),
    path('walletmoney/<int:wallet_id>/', WalletDetailsApiView.as_view()),

]