from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from address.serializers import AddressSerializer, InsuranceSerializer
from .models import Practice, PracticeServices, PracticeMembershipsAndAffiliations


class PracticeSerializer(ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = Practice
        exclude = ['date_created', 'last_updated', 'accessibility']


class PracticeGetSerializer(ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()
    accepted_insurances = InsuranceSerializer( many=True)

    class Meta:
        model = Practice
        exclude = ['date_created', 'last_updated']


class PracticeServicesSerializer(ModelSerializer):
    class Meta:
        model = PracticeServices
        exclude = ['date_created', 'last_updated']


class PracticeUpdateSerializer(ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Practice
        exclude = ['date_created', 'last_updated']


class PracticeUpdateAdminSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Practice
        fields = ['pk', 'user']


class PracticeMembershipsAndAffiliationsSerializer(ModelSerializer):
    class Meta:
        model = PracticeMembershipsAndAffiliations
        exclude = ['date_created', 'last_updated']
