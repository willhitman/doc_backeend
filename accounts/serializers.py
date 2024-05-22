from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Doctor.models import Doctor, Insurance
from accounts.models import User, UserServiceAccounts
from practice.models import Practice


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['userId'] = user.id
        token['firstName'] = user.first_name
        token['lastName'] = user.last_name

        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'gender', 'email']


class DoctorInsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        exclude = ['date_created', 'last_updated']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'date_of_birth', 'last_name', 'gender', 'email']


class UserServiceAccountsSerializer(ModelSerializer):
    class Meta:
        model = UserServiceAccounts
        exclude = ['date_created', 'last_updated']
