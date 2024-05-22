from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers

from Doctor.models import Doctor, DoctorSpecialization, DoctorLanguages, DoctorAffiliationsAndMemberships, \
    DoctorEducationalBackground
from accounts.models import User
from accounts.serializers import UserSerializer
from address.models import Address, Services
from address.serializers import AddressSerializer


class AddressCreateSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ['date_created', 'last_updated']


class DoctorUpdateSerializer(ModelSerializer):
    address = AddressCreateSerializer()
    class Meta:
        model = Doctor
        exclude = ['date_create', 'last_updated']

    def update(self, instance, validated_data):
        languages = validated_data.pop("languages")

        # Update doctor
        instance.languages.set(languages)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class DoctorCreateSerializer(ModelSerializer):
    address = AddressCreateSerializer()

    class Meta:
        model = Doctor
        exclude = ['date_create', 'last_updated', 'languages']

    def create(self, validated_data):
        doctor = Doctor.objects.create(**validated_data)
        return doctor


class DoctorSerializer(ModelSerializer):
    user = UserSerializer()
    address = AddressCreateSerializer()

    class Meta:
        model = Doctor
        exclude = ['date_create', 'last_updated']


class DoctorSpecializationSerializer(ModelSerializer):
    class Meta:
        model = DoctorSpecialization
        exclude = ['date_create', 'last_updated']


class DoctorLanguagesSerializer(ModelSerializer):
    class Meta:
        model = DoctorLanguages
        exclude = ['date_create', 'last_updated', 'proficiency']


class DoctorGetSerializer(ModelSerializer):
    languages = DoctorLanguagesSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Doctor
        exclude = ['date_create', 'last_updated']


class DoctorAffiliationSerializer(ModelSerializer):
    class Meta:
        model = DoctorAffiliationsAndMemberships
        exclude = ['date_create', 'last_updated']


class DoctorEducationalBackgroundSerializer(ModelSerializer):
    class Meta:
        model = DoctorEducationalBackground
        exclude = ['date_create', 'last_updated']


class ServicesSerializer(ModelSerializer):
    class Meta:
        model = Services
        exclude = ['date_create', 'last_updated']


class DoctorSearchByNameSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'phone_number', 'linkedin', 'address', 'title',
                  'profile_picture',
                  'languages']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        affiliations = DoctorAffiliationsAndMemberships.objects.filter(doctor=instance)
        representation['affiliations'] = DoctorAffiliationSerializer(affiliations, many=True).data
        return representation

# class DoctorSearchBySpecializationSerializer(ModelSerializer):
#     doctor = DoctorGetSerializer()
#
#     class Meta:
#         model = DoctorPracticeLocationInfo
#         fields = ['id', 'doctor', 'address',
#                   'contact_phone_number', 'contact_email', 'whatsapp_number', 'office_hours']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         practice = DoctorPracticeLocationInfo.objects.filter(doctor=instance.doctor)
#         affiliations = DoctorAffiliationsAndMemberships.objects.filter(doctor=instance.doctor)
#         specialization = DoctorSpecialization.objects.filter(doctor=instance.doctor)
#         representation['affiliations'] = DoctorAffiliationSerializer(affiliations, many=True).data
#         representation['specialization'] = DoctorSpecializationSerializer(specialization, many=True).data
#         return representation


# class DoctorSearchByLocationSerializer(ModelSerializer):
#     doctor = DoctorGetSerializer()
#     affiliations = DoctorAffiliationSerializer(many=True)
#     specialization = DoctorSpecializationSerializer(many=True)
#
#     class Meta:
#         model = DoctorPracticeLocationInfo
#         fields = ['id', 'doctor', 'services', 'affiliations', 'specialization', 'address',
#                   'contact_phone_number', 'contact_email', 'whatsapp_number', 'office_hours']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         affiliations = DoctorAffiliationsAndMemberships.objects.filter(doctor=instance.doctor)
#         specialization = DoctorSpecialization.objects.filter(doctor=instance.doctor)
#         representation['affiliations'] = DoctorAffiliationSerializer(affiliations, many=True).data
#         representation['specialization'] = DoctorSpecializationSerializer(specialization, many=True).data
#         return representation
