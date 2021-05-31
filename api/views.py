from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.models import ContactUs, Feedback, Notification, Setup, Transaction, User, Wallet
from api.serializers import ContactUsSerializer, NotificationSerializer, SetupSerializer, TransactionSerializer, UserSerializer, UserFeedbackSerializer, WalletSerializer
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
import datetime
from django.core import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
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
            'city': request.data.get('city'), 
            'zip': request.data.get('zip'), 
            'photo': request.data.get('photo'),
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
            'city': request.data.get('city'), 
            'zip': request.data.get('zip'), 
            'photo': request.data.get('photo'),
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
            'occupiedBy': ''
        }
        serializer = SetupSerializer(instance = setup_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data, 'saved data')
            # note = {
            # 'text': 'this is test notification', 
            # 'isRead': 'False',
            # 'setup': '1',
            # 'user': request.user.id,
            # }
            # print(note, 'notification data')
            # serializer_notification = NotificationSerializer(data=note)
            # if serializer_notification.is_valid():
            #     serializer_notification.save()
            #     print(serializer_notification, 'notify')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationApiView(APIView):
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
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, notify_id):
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
        serializer = NotificationSerializer(instance = notify_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, notify_id, *args, **kwargs):
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
            'user': request.user.id
        }
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            data = Setup.objects.filter(id=serializer.data['setup'])

            for i in data:
                data.update(isOccupied=True)
                data.update(occupiedBy=request.user.id)

            serialized_qs = serializers.serialize('json', data)
            send = {
                "data":serializer.data,
                "setup": serialized_qs
            }
            
            # serialized_qs = serializers.serialize('json', send)
            print(serializer.data, 'serializer data')
            print(send, 'send data')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NearMeApiView(APIView):
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletDetailsApiView(APIView):
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
        print(wallet_instance, 'wallet instance')
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
            print(int(request.data.get('balance')), 'requested balance')
            print(int(serializer.data['balance']), 'serialized balance')
            plus = int(request.data.get('balance')) + int(serializer.data['balance'])
            print(plus, 'added value')
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