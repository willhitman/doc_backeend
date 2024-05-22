from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from Doctor.serializers import AddressCreateSerializer
from Locum.models import Locum, LocumLanguages, LocumSpecialization, LocumAffiliations, LocumEducationalBackground
from accounts.serializers import UserSerializer
from address.serializers import AddressSerializer


class LocumLanguagesSerializer(ModelSerializer):
    class Meta:
        model = LocumLanguages
        exclude = ['date_created', 'last_updated']


class LocumSerializer(ModelSerializer):
    address = AddressCreateSerializer()

    class Meta:
        model = Locum
        exclude = ['date_created', 'last_updated','languages']


class LocumSpecializationSerializer(ModelSerializer):
    class Meta:
        model = LocumSpecialization
        exclude = ['date_created', 'last_updated']


class LocumMembershipsAndAffiliationsSerializer(ModelSerializer):
    class Meta:
        model = LocumAffiliations
        exclude = ['date_created', 'last_updated']


class LocumEducationalBackgroundSerializer(ModelSerializer):
    class Meta:
        model = LocumEducationalBackground
        exclude = ['date_created', 'last_updated']
