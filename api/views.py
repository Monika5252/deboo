from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.models import ContactUs, Feedback, Setup, User
from api.serializers import ContactUsSerializer, SetupSerializer, UserSerializer, UserFeedbackSerializer
from api.permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
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