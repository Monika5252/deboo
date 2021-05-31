from django.conf.urls import url, include
from rest_framework import routers
from api.views import ContactApiView, ContactUsApiView, FeedbackApiView, FeedbackDetailsApiView, NearMeApiView, NotificationApiView, NotificationDetailsApiView, OccupySetupView, SetupApiView, SetupDetailsApiView, TransactionsApiView, UserViewSet
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

    url(r'^nearme/', NearMeApiView.as_view())
]