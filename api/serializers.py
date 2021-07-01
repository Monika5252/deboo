
from api.models import AdminNotification, ContactUs, Feedback, InOutCount, Notification, Setup, SetupTransactionSuccess, StaffProfile, Transaction, User, UserProfile, Wallet, WalletTransaction

from rest_framework.serializers import ModelSerializer

class UserProfileSerializer(ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('id', 'name','fcm_token', 'birthdate', 'age', 'address', 'country', 'gender', 'city', 'zip', 'photo','isWallet','user_type')

class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'mobile', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        profile.name = profile_data.get('name', profile.name)
        profile.fcm_token = profile_data.get('fcm_token', profile.fcm_token)
        profile.birthdate = profile_data.get('birthdate', profile.birthdate)
        profile.age = profile_data.get('age', profile.age)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.isWallet = profile_data.get('isWallet', profile.isWallet)

        profile.user_type = profile_data.get('user_type', profile.user_type)
        profile.save()

        return instance

class UserFeedbackSerializer(ModelSerializer):
    userDetails = UserSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = ('id','mobile', 'rate', 'text', 'userDetails','createdAt','updatedAt')

class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('id','contact','mobile')

class SetupSerializer(ModelSerializer):
    class Meta:
        model = Setup
        fields = ('__all__')

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('__all__')

class WalletTransactionSerializer(ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = ('__all__')

class NotificationSerializer(ModelSerializer):
    setupDetails = SetupSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ('id','text','isRead', 'setup','setupDetails','user','createdAt','updatedAt')

class AdminNotificationSerializer(ModelSerializer):
    setupDetails = SetupSerializer(read_only=True)
    class Meta:
        model = AdminNotification
        fields = ('id','text','isRead', 'setup','setupDetails','user','createdAt','updatedAt')


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('__all__')

class StaffSerializer(ModelSerializer):
    setupDetails = SetupSerializer(read_only=True)
    class Meta:
        model = StaffProfile
        fields = ('id', 'name','mobile', 'adhaar', 'setup', 'setupDetails', 'age', 'address', 'gender', 'country', 'state', 'city', 'zip', 'photo')

class InOutCountSerializer(ModelSerializer):
    setupDetails = SetupSerializer(read_only=True)
    class Meta:
        model = InOutCount
        fields = ('inSetup','outSetup', 'setup', 'setupDetails', 'createdAt','updatedAt')