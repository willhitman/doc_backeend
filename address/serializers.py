from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ModelSerializer

from address.models import Address, Insurance


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ['date_created', 'last_updated']


class InsuranceSerializer(ModelSerializer):
    class Meta:
        model = Insurance
        exclude = ['date_created', 'last_updated']
