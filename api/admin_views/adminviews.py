from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import ContactUs, Feedback, InOutCount, Notification, Setup, StaffProfile, Transaction, User, UserProfile, Wallet
from api.serializers import ContactUsSerializer, InOutCountSerializer, NotificationSerializer, SetupSerializer, StaffSerializer, TransactionSerializer, UserSerializer, UserFeedbackSerializer, WalletSerializer

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from django.core import serializers
from fcm_django.models import FCMDevice
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from api.utils import generate_access_token, generate_refresh_token
from rest_framework import exceptions
import jwt
from django.conf import settings

from django.views.decorators.csrf import csrf_protect
from rest_framework import exceptions


class AdminNotificationApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Notifications
        '''
        notify = Notification.objects.all()
        serializer = NotificationSerializer(notify, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminInOutCountApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the In Out count
        '''
        inOut = InOutCount.objects.all()
        serializer = InOutCountSerializer(inOut, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

