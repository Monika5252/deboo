from django.conf.urls import url, include
from rest_framework import routers
from api.views import ContactApiView, ContactUsApiView, FeedbackApiView, FeedbackDetailsApiView, UserViewSet
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
]