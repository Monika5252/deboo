from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import ContactUs, Feedback, Notification, Setup, StaffProfile, Transaction, User, UserProfile, Wallet, WalletTransaction
from api.serializers import AdminNotificationSerializer, ContactUsSerializer, NotificationSerializer, SetupSerializer, StaffSerializer, TransactionSerializer, UserSerializer, UserFeedbackSerializer, WalletSerializer, WalletTransactionSerializer

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from django.core import serializers
from fcm_django.models import FCMDevice
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from api.utils import generate_access_token, generate_refresh_token
from rest_framework import exceptions
import jwt
from django.conf import settings

from django.http.response import JsonResponse

from rest_framework import exceptions

@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_protect
def refresh_token_view(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})


@api_view(['POST'])
@permission_classes([AllowAny])
# @ensure_csrf_cookie
def login_view(request):
    User = get_user_model()
    mobile = request.data.get('mobile')
    password = request.data.get('password')
    user_type = request.data.get('user_type')
    response = Response()
    if (mobile is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'credentials required')

    user = User.objects.filter(mobile=mobile).first()
    if(user is None and user_type!='1'):
        # user = User.objects.create(mobile=mobile, password=password)
        # user.save()
        # print(user,"user")
        # serialized_user = UserSerializer(user,context={'request': request}).data
        # print(serialized_user)
        user = User(mobile=mobile, password=password)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user,user_type=0)
    
    if(user is None and user_type == '1'):
        return Response(
                {"res": "Admin with these credentials does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if(user and user_type == '1'):
        if user.check_password(password):
            serialized_user = UserSerializer(user,context={'request': request}).data
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            response.data = {
                'token': access_token,
                'user_id':serialized_user['profile']['id'],
                'name':serialized_user['profile']['name'],
                'email':serialized_user['email'],
                'first_name': serialized_user['first_name'],
                'type': serialized_user['profile']['user_type'],
                'last_name': serialized_user['last_name'],
                'mobile': serialized_user['mobile'],
                'user': serialized_user
                }
            return response
        else:
            raise exceptions.AuthenticationFailed(
            'Bad credentials')

    if(user and user_type!='1'):
        user = User.objects.filter(mobile=mobile).first()
        # raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
            
        serialized_user = UserSerializer(user,context={'request': request}).data
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
        'token': access_token,
        'user_id':serialized_user['profile']['id'],
        'name':serialized_user['profile']['name'],
        'email':serialized_user['email'],
        'first_name': serialized_user['first_name'],
        'type': serialized_user['profile']['user_type'],
        'last_name': serialized_user['last_name'],
        'mobile': serialized_user['mobile'],
        'user': serialized_user
        }
        
        return response

@api_view(['POST'])
@permission_classes([AllowAny])
# @csrf_protect
def forget_password_token(request):

    try:
        user = User.objects.get(mobile=request.data.get('mobile'))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code
    def get_permissions(self):
        permission_classes = []
        # if self.action == 'create':
        #     permission_classes = [AllowAny]
        # elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
        #     permission_classes = [IsLoggedInUserOrAdmin]
        # elif self.action == 'list' or self.action == 'destroy':
        #     permission_classes = [IsAdminUser]
        # return [permission() for permission in permission_classes]

        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [AllowAny]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

class FeedbackApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Feedbacks
        '''
        feed = Feedback.objects.all()
        serializer = UserFeedbackSerializer(feed, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create Feedback with given data
        '''
        data = {
            'mobile': request.data.get('mobile'), 
            'rate': request.data.get('rate'), 
            'text': request.data.get('text'),
            'user': request.user.id
        }
        serializer = UserFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackDetailsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, feed_id, user_id):
        '''
        Helper method to get the object with given feedback id and user_id
        '''
        try:
            return Feedback.objects.get(id=feed_id, user = user_id)
        except Feedback.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, feed_id, *args, **kwargs):
        '''
        Retrieves the Feedback with given feedback id
        '''
        feed_instance = self.get_object(feed_id, request.user.id)
        if not feed_instance:
            return Response(
                {"res": "Object with this feedback id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserFeedbackSerializer(feed_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, feed_id, *args, **kwargs):
        '''
        Updates the feedback item with given feedback id if exists
        '''
        feed_instance = self.get_object(feed_id, request.user.id)
        if not feed_instance:
            return Response(
                {"res": "Object with this feedback id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'mobile': request.data.get('mobile'), 
            'rate': request.data.get('rate'),
            'text': request.data.get('text'),
            'user': request.user.id
        }
        serializer = UserFeedbackSerializer(instance = feed_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, feed_id, *args, **kwargs):
        '''
        Deletes the Feedback with given feedback id if exists
        '''
        feed_instance = self.get_object(feed_id, request.user.id)
        if not feed_instance:
            return Response(
                {"res": "Object with this feedback id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        feed_instance.delete()
        return Response(
            {"res": "Feedback deleted!"},
            status=status.HTTP_200_OK
        )


class ContactApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Contact Us data
        '''
        contact = ContactUs.objects.all()
        serializer = ContactUsSerializer(contact, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create Contact info with given data
        '''
        data = {
            'contact': request.data.get('contact'), 
            'mobile': request.data.get('mobile')
        }
        serializer = ContactUsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactUsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, contact_id):
        '''
        Helper method to get the object with given contact_id
        '''
        try:
            return ContactUs.objects.get(id=contact_id)
        except ContactUs.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, contact_id, *args, **kwargs):
        '''
        Retrieves the Contact us with given contact id
        '''
        contact_instance = self.get_object(contact_id)
        if not contact_instance:
            return Response(
                {"res": "Record with this contact id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ContactUsSerializer(contact_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, contact_id, *args, **kwargs):
        '''
        Updates the Contact details with given contact id if exists
        '''
        contact_instance = self.get_object(contact_id)
        if not contact_instance:
            return Response(
                {"res": "Record with this contact id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'contact': request.data.get('contact'), 
            'mobile': request.data.get('mobile')
        }
        serializer = ContactUsSerializer(instance = contact_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, contact_id, *args, **kwargs):
        '''
        Deletes the Contact details with given contact id if exists
        '''
        contact_instance = self.get_object(contact_id)
        if not contact_instance:
            return Response(
                {"res": "Object with this contact id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        contact_instance.delete()
        return Response(
            {"res": "Contact deleted!"},
            status=status.HTTP_200_OK
        )


class SetupApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Setups data
        '''
        setup = Setup.objects.all()
        serializer = SetupSerializer(setup, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create Setup with given data
        '''

        data = {
            'name': request.data.get('name'), 
            'address': request.data.get('address'),
            'longitude': request.data.get('longitude'), 
            'latitude': request.data.get('latitude'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'), 
            'zip': request.data.get('zip'), 
            'photo': request.data.get('photo'),
            'fees': request.data.get('fees'),
            'isOccupied': request.data.get('isOccupied'),
            'isCleaned': request.data.get('isCleaned'), 
            'createdBy': request.user.id,
            'updatedBy': request.user.id
        }
        serializer = SetupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetupDetailsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, setup_id):
        '''
        Helper method to get the object with given setup id
        '''
        try:
            return Setup.objects.get(id=setup_id)
        except Setup.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, setup_id):
        '''
        Retrieves the Contact us with given contact id
        '''
        setup_instance = self.get_object(setup_id)
        if not setup_instance:
            return Response(
                {"res": "Record with this Setup id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SetupSerializer(setup_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, setup_id, *args, **kwargs):
        '''
        Updates the setup details with given setup id if exists
        '''
        setup_instance = self.get_object(setup_id)
        if not setup_instance:
            return Response(
                {"res": "Record with this setup id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'address': request.data.get('address'),
            'longitude': request.data.get('longitude'), 
            'latitude': request.data.get('latitude'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'), 
            'zip': request.data.get('zip'), 
            'photo': request.data.get('photo'),
            'isActive': request.data.get('isActive'),
            'isDeleted': request.data.get('isDeleted'),
            'isOccupied': request.data.get('isOccupied'),
            'isCleaned': request.data.get('isCleaned'),
            'updatedBy': request.user.id
        }
        serializer = SetupSerializer(instance = setup_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, setup_id, *args, **kwargs):
        '''
        Deletes Setup details with given setup id if exists
        '''
        setup_instance = self.get_object(setup_id)
        if not setup_instance:
            return Response(
                {"res": "Object with this setup id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        setup_instance.delete()
        return Response(
            {"res": "Setup deleted!"},
            status=status.HTTP_200_OK
        )

class OccupySetupView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, setup_id):
        '''
        Helper method to get the object with given setup id
        '''
        try:
            return Setup.objects.get(id=setup_id)
        except Setup.DoesNotExist:
            return None

    def put(self, request, setup_id, *args, **kwargs):
        '''
        Updates the setup details with given setup id if exists
        '''
        setup_instance = self.get_object(setup_id)
        if not setup_instance:
            return Response(
                {"res": "Record with this setup id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'isOccupied': request.data.get('isOccupied'),
            'occupiedBy': request.user.id
        }
        data = Setup.objects.filter(id=setup_id)

        for i in data:
            data.update(isOccupied=False)
            data.update(isTransactionComplete=False)
        PushNotifyRelease(request.user.id)
        # ReleaseNotification(request.user.id, setup_id)
        # serializer = SetupSerializer(instance = setup_instance, data=data, partial = True)
        # if serializer.is_valid():
        #     serializer.save() 
        #     PushNotifyRelease(request.user.id)
        #     ReleaseNotification(request.user.id, serializer.data['id'])
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

class NotificationApiView(APIView):
    permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Notifications data
        '''
        notify = Notification.objects.filter(user=request.user.id)
        serializer = NotificationSerializer(notify, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationDetailsApiView(APIView):
    permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, notify_id):
        '''
        Helper method to get the object with given setup id
        '''
        try:
            return Notification.objects.get(id=notify_id)
        except Notification.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, notify_id, *args, **kwargs):
        '''
        Retrieves the Notification with given notify id
        '''
        notify_instance = self.get_object(notify_id)
        if not notify_instance:
            return Response(
                {"res": "Notification with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NotificationSerializer(notify_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, notify_id, *args, **kwargs):
        '''
        Updates the Notification details with given notify id if exists
        '''
        notify_instance = self.get_object(notify_id)
        if not notify_instance:
            return Response(
                {"res": "Notification with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'isRead': request.data.get('isRead')
        }
        print(data, 'data get')
        serializer = NotificationSerializer(instance = notify_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, notify_id, request, *args, **kwargs):
        '''
        Deletes Notification details with given id if exists
        '''
        notify_instance = self.get_object(notify_id)
        if not notify_instance:
            return Response(
                {"res": "Notification with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        notify_instance.delete()
        return Response(
            {"res": "Notification deleted!"},
            status=status.HTTP_200_OK
        )

class TransactionsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Transactions data
        '''
        transaction = Transaction.objects.filter(user=request.user.id)
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create Transaction with given data
        '''

        data = {
            'transaction_id': request.data.get('transaction_id'),
            'money': request.data.get('money'),
            'mobile': request.data.get('mobile'),
            'setup': request.data.get('setup'),
            'user': request.user.id,
            'w_id': request.data.get('w_id')
        }
        
        # wallet_money = request.data.get('walletMoney')
        # wallet_id = request.data.get('w_id')
        # print(wallet_money)

        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            get_wallet = Wallet.objects.filter(id=request.data.get('w_id'))
            
            # wallet_serializer = WalletSerializer(get_wallet, many=True)

            for i in get_wallet:
                get_wallet.update(balance=i.balance-int(request.data.get('money')))

            data = Setup.objects.filter(id=serializer.data['setup'])

            wallet_data = Wallet.objects.filter(id=serializer.data['w_id'])

            for i in data:
                data.update(isOccupied=True)
                data.update(isTransactionComplete=True)
                data.update(occupiedBy=request.user.id)

            serialized_qs = serializers.serialize('json', data)
            serialized_wallet = serializers.serialize('json', wallet_data)
            send = {
                "data":serializer.data,
                "setup": serialized_qs,
                "wallet": serialized_wallet
            }

            PushNotifyBook(request.user.id)
            PushNotifyAdmin()
            BookNotification(request.user.id, request.data.get('setup'))
            BookNotificationAdmin(request.user.id, request.data.get('setup'))
            # serialized_qs = serializers.serialize('json', send)
            
            return Response(send, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetailsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, transaction_id):
        '''
        Helper method to get the object with given transaction id
        '''
        try:
            return Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, transaction_id, *args, **kwargs):
        '''
        Retrieves the Transaction with given notify id
        '''
        notify_instance = self.get_object(transaction_id)
        if not notify_instance:
            return Response(
                {"res": "Transaction with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TransactionSerializer(notify_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, transaction_id, *args, **kwargs):
        '''
        Updates the Transaction details with given transaction id if exists
        '''
        notify_instance = self.get_object(transaction_id)
        if not notify_instance:
            return Response(
                {"res": "Transaction with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'isRead': request.data.get('isRead')
        }
        serializer = TransactionSerializer(instance = notify_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, transaction_id, *args, **kwargs):
        '''
        Deletes Transaction details with given id if exists
        '''
        notify_instance = self.get_object(transaction_id)
        if not notify_instance:
            return Response(
                {"res": "Transaction with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        notify_instance.delete()
        return Response(
            {"res": "Transaction deleted!"},
            status=status.HTTP_200_OK
        )


class WalletTransactionDetailsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, wallet_id):
        '''
        Helper method to get the object with given wallet id
        '''
        try:
            return WalletTransaction.objects.get(id=wallet_id)
        except WalletTransaction.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, wallet_id, *args, **kwargs):
        '''
        Retrieves the Transaction with given wallet id
        '''
        wallet_instance = self.get_object(wallet_id)
        if not wallet_instance:
            return Response(
                {"res": "Transaction with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = WalletTransactionSerializer(wallet_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 5. Delete
    def delete(self, request, wallet_id, *args, **kwargs):
        '''
        Deletes Transaction details with given id if exists
        '''
        wallet_instance = self.get_object(wallet_id)
        if not wallet_instance:
            return Response(
                {"res": "Transaction with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        wallet_instance.delete()
        return Response(
            {"res": "Wallet Transaction deleted!"},
            status=status.HTTP_200_OK
        )


class WalletTransactionsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the Wallet Transactions data
        '''
        wallet = WalletTransaction.objects.filter(user=request.user.id)
        serializer = WalletTransactionSerializer(wallet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Create Wallet Transaction with given data
        '''

        data = {
            'transaction_id': request.data.get('transaction_id'),
            'amount': request.data.get('amount'),
            'mobile': request.data.get('mobile'),
            'setup': request.data.get('setup'),
            'wallet_id': request.data.get('w_id'),
            'user': request.user.id,
            'w_id': request.data.get('w_id')
        }

        serializer = WalletTransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            data = Setup.objects.filter(id=serializer.data['setup'])

            wallet_data = Wallet.objects.filter(id=serializer.data['w_id'])

            for i in data: 
                data.update(isOccupied=True)
                data.update(isTransactionComplete=True)
                data.update(occupiedBy=request.user.id)

            serialized_qs = serializers.serialize('json', data)
            serialized_wallet = serializers.serialize('json', wallet_data)
            send = {
                "data":serializer.data,
                "setup": serialized_qs,
                "wallet": serialized_wallet
            }

            PushNotifyBook(request.user.id)
            PushNotifyAdmin()
            BookNotification(request.user.id, request.data.get('setup'))
            BookNotificationAdmin(request.user.id, request.data.get('setup'))
            # serialized_qs = serializers.serialize('json', send)
            
            return Response(send, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NearMeApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the near by setups data
        '''
        data = []
        allSetup = Setup.objects.all()
        # print(allSetup)
        for i in allSetup:
            data.append(
                {
                'id':i.id,
                'name':i.name,
                'longitude':i.longitude,
                'latitude':i.latitude
            })
        # print(data, 'dict')
            # print(i.latitude, 'latitude')
        # serializer = NotificationSerializer(allSetup, many=True)
        # if serializer
        return Response(data, status=status.HTTP_200_OK)

class WalletApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List User Wallet
        '''
        balance = Wallet.objects.filter(user=request.user.id)
        serializer = WalletSerializer(balance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create Wallet with given data
        '''
        data = {
            'balance': request.data.get('balance'), 
            'user': request.user.id
        }
        serializer = WalletSerializer(data=data)
        if serializer.is_valid():
            userData = UserProfile.objects.filter(id=request.user.id)
            print(userData)
            for d in userData:
                userData.update(isWallet=True)
                print(d, 'user details')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletDetailsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, wallet_id):
        '''
        Helper method to get the object with given wallet id
        '''
        try:
            return Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, wallet_id, *args, **kwargs):
        '''
        Retrieves the Wallet with given wallet id
        '''
        wallet_instance = self.get_object(wallet_id)
        if not wallet_instance:
            return Response(
                {"res": "Wallet with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = WalletSerializer(wallet_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, wallet_id, *args, **kwargs):
        '''
        Updates the Wallet balance with given wallet id if exists
        '''
        wallet_instance = self.get_object(wallet_id)
        
        if not wallet_instance:
            return Response(
                {"res": "Wallet with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'balance': request.data.get('balance')
        }
        serializer = WalletSerializer(instance = wallet_instance, data=data, partial = True)
        if serializer.is_valid():
            # serializer.save()
            data = Wallet.objects.filter(id=serializer.data['id'])

            plus = int(request.data.get('balance')) + int(serializer.data['balance'])
            
            for i in data:
                data.update(balance=int(request.data.get('balance'))+int(serializer.data['balance']))
            
            serialized_qs = serializers.serialize('json', data)
            return Response(serialized_qs, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, notify_id, *args, **kwargs):
        '''
        Deletes Wallet details with given id if exists
        '''
        wallet_instance = self.get_object(notify_id)
        if not wallet_instance:
            return Response(
                {"res": "Wallet with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        wallet_instance.delete()
        return Response(
            {"res": "Wallet deleted!"},
            status=status.HTTP_200_OK
        )

def BookNotification(user, setup):
    note = {
    'text': 'You have booked ' + setup + ' this setup.',
    'isRead': 'False',
    'setup': setup,
    'user': user,
    }

    serializer_notification = NotificationSerializer(data=note)
    if serializer_notification.is_valid():
        serializer_notification.save()
    return True

def BookNotificationAdmin(user, setup):
    note = {
    'text':  'A user has booked ' + setup + ' this setup.',
    'isRead': 'False',
    'setup': setup,
    'user': user,
    }

    serializer_notification = AdminNotificationSerializer(data=note)
    if serializer_notification.is_valid():
        serializer_notification.save()
    return True

def ReleaseNotification(user, setup):
    note = {
    'text': 'Thank you for using our service. on ' + setup + 'this setup.', 
    'isRead': 'False',
    'setup': setup,
    'user': user,
    }
    serializer_notification = NotificationSerializer(data=note)
    if serializer_notification.is_valid():
        serializer_notification.save()
    return True

def PushNotifyBook(uid):
    user_data = User.objects.filter(id=uid)
    device = FCMDevice()
    for i in user_data:
        device.registration_id = i.profile.fcm_token
    device.name = "Deboo Android"
    device.save()
    device.send_message(
        title="Deboo",
        body="you have booked a service",
        data={
            "notification type" : 20
        })
    print(device)
    return True

def PushNotifyAdmin():
    user_data = UserProfile.objects.filter(user_type=1)
    device = FCMDevice()
    for i in user_data:
        device.registration_id = i.fcm_token
    device.name = "Deboo Android"
    device.save()
    device.send_message(
        title="Deboo",
        body="A user has booked a service",
        data={
            "notification type" : 20
        })
    print(device)
    return True

def PushNotifyRelease(uid):
    user_data = User.objects.filter(id=uid)
    device = FCMDevice()
    for i in user_data:
        device.registration_id = i.profile.fcm_token
    device.name = "Deboo Android"
    device.save()
    device.send_message(
        title="Deboo",
        body="Thank you for using our service",
        data={
            "notification type" : 20
        })
    print(device)
    return True
 
class AllTransactionApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List All Transactions
        '''
        transaction = Transaction.objects.all()
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetStaffApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List All Staff
        '''
        staff = StaffProfile.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create Staff with given data
        '''

        data = {
            'name': request.data.get('name'), 
            'address': request.data.get('address'),
            'mobile': request.data.get('mobile'), 
            'zip': request.data.get('zip'), 
            'photo': request.data.get('photo'),
            'adhaar': request.data.get('adhaar'),
            'age': request.data.get('age'), 
            'gender': request.data.get('gender'),
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'),
            'setup': request.data.get('setup_id')
        }
        serializer = StaffSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            data = Setup.objects.filter(id=request.data.get('setup_id'))

            for i in data:
                print(i)
                data.update(staff=serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffDetailsApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, staff_id):
        '''
        Helper method to get the object with given staff id
        '''
        try:
            return StaffProfile.objects.get(id=staff_id)
        except StaffProfile.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, staff_id, *args, **kwargs):
        '''
        Retrieves the Staff Profile with given staff id
        '''
        staff_instance = self.get_object(staff_id)
        if not staff_instance:
            return Response(
                {"res": "Staff with this id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaffSerializer(staff_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, staff_id, *args, **kwargs):
        '''
        Updates the Staff Profile details with given staff id if exists
        '''
        staff_instance = self.get_object(staff_id)
        if not staff_instance:
            return Response(
                {"res": "Staff with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'), 
            'address': request.data.get('address'),
            'mobile': request.data.get('mobile'), 
            'zip': request.data.get('zip'), 
            'photo': request.data.get('photo'),
            'adhaar': request.data.get('adhaar'),
            'age': request.data.get('age'), 
            'gender': request.data.get('gender'),            
            'country': request.data.get('country'),
            'state': request.data.get('state'),
            'city': request.data.get('city'),
            'setup': request.data.get('setup_id')
        }
        serializer = StaffSerializer(instance = staff_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, staff_id, *args, **kwargs):
        '''
        Deletes Staff profile details with given id if exists
        '''
        staff_instance = self.get_object(staff_id)
        if not staff_instance:
            return Response(
                {"res": "Staff profile with this id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        staff_instance.delete()
        return Response(
            {"res": "Staff Profile deleted!"},
            status=status.HTTP_200_OK
        )

class CityStateListView(APIView):
    def get(self, request):
        fh = open(settings.CITY_STATE_FILE)
        data = fh.read()
        import json
        return JsonResponse(json.loads(data), safe=False)