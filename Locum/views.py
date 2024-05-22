from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from Locum.models import Locum, LocumSpecialization, LocumAffiliations, LocumEducationalBackground
from Locum.serializers import LocumSerializer, LocumSpecializationSerializer, LocumMembershipsAndAffiliationsSerializer, \
    LocumEducationalBackgroundSerializer
from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.service_account_manager import save_user_service_accounts
from address.models import Address
from address.serializers import AddressSerializer


# Create your views here.

class LocumCreateView(GenericAPIView):
    serializer_class = LocumSerializer
    queryset = Locum.objects.all()

    def post(self, request):
        data = {
            'user': None if request.data.get('user_id') == '' else request.data.get('user_id'),
            'national_id': None if request.data.get('national_id') == '' else request.data.get('national_id'),
            'phone_number': None if request.data.get('phone_number') == '' else request.data.get('phone_number'),
            'linkedin': None if request.data.get('linkedin') == '' else request.data.get('linkedin'),
            'title': None if request.data.get('title') == '' else request.data.get('title'),
            'bio': None if request.data.get('bio') == '' else request.data.get('bio'),
            'website': None if request.data.get('website') == '' else request.data.get('website'),

            'profile_picture': None if request.data.get('profile_picture') == '' else request.data.get(
                'profile_picture'),
            'languages': None if request.data.get('languages') == '' else request.data.get('languages'),

        }
        address = {
            'door_address': None if request.data.get('door_address') == '' else request.data.get(
                'door_address'),
            'street_one': None if request.data.get('street_one') == '' else request.data.get('street_one'),
            'street_two': None if request.data.get('street_two') == '' else request.data.get('street_two'),
            'suburb': None if request.data.get('suburb') == '' else request.data.get('suburb'),
            'province': None if request.data.get('province') == '' else request.data.get('province'),
            'city': None if request.data.get('city') == '' else request.data.get('city'),
        }
        serializer = self.serializer_class(data=data, partial=True)
        address_serializer = AddressSerializer(data = address, partial=True)

        if serializer.is_valid():
            saved_locum = serializer.save()
            if address_serializer.is_valid():
                saved_address = address_serializer.save()
                saved_locum.address = saved_address
            saved_locum.save()
            # create service account reference
            save_user_service_accounts(saved_locum.user, Locum, saved_locum.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocumReadUpdateDestroyView(GenericAPIView):
    serializer_class = LocumSerializer
    queryset = Locum.objects.all()

    def get(self, request, pk):
        try:
            locum = Locum.objects.get(pk=pk)
        except Locum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(locum)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            locum = Locum.objects.get(pk=pk)
        except Locum.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.data.pop('user')
        serializer = self.serializer_class(locum, data=request.data, partial=True)

        if serializer.is_valid():
            address = serializer.validated_data.pop('address')
            _user = User.objects.get(pk=locum.user.pk)
            user_serializer = UserSerializer(_user, data=user, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

            # check address exists?
            try:
                _address = Address.objects.get(pk=locum.address.pk)
            except Address.DoesNotExist:
                address = Address.objects.create(**address)
                saved = serializer.save()
                saved.address = address
                saved.save()
            else:
                address_serializer = AddressSerializer(_address, data=address, partial=True)
                if address_serializer.is_valid():
                    address_serializer.save()
                else:
                    print(serializer.errors)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            locum = Locum.objects.get(pk=pk)
        except Locum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        locum.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LocumGetByUserIdView(GenericAPIView):
    serializer_class = LocumSerializer
    queryset = Locum.objects.all()

    def get(self, request, user_id):
        try:
            locum = Locum.objects.get(user=user_id)
        except Locum.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(locum)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocumSpecializationCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumSpecializationSerializer
    queryset = LocumSpecialization.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocumSpecializationReadUpdateDestroyView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumSpecializationSerializer
    queryset = LocumSpecialization.objects.all()

    def get(self, request, pk):
        try:
            specialization = self.queryset.get(pk=pk)
        except LocumSpecialization.DoesNotExist:
            return Response({'error': 'Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(specialization)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            specialization = self.queryset.get(pk=pk)
        except LocumSpecialization.DoesNotExist:
            return Response({'error': 'Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(specialization, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            specialization = self.queryset.get(pk=pk)
        except LocumSpecialization.DoesNotExist:
            return Response({'error': 'Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            specialization.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class LocumSpecializationGetByUserIdView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumSpecializationSerializer
    queryset = LocumSpecialization.objects.all()

    def get(self, request, pk):
        specializations = self.queryset.filter(locum__user__id=pk)
        if specializations.exists():
            serializer = self.serializer_class(specializations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Specializations not found'}, status=status.HTTP_400_BAD_REQUEST)


class LocumMembershipsAndAffiliationsCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumMembershipsAndAffiliationsSerializer
    queryset = LocumAffiliations.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocumMembershipsAndAffiliationsReadUpdateDestroyView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumMembershipsAndAffiliationsSerializer
    queryset = LocumAffiliations.objects.all()

    def get(self, request, pk):
        try:
            membership = self.queryset.get(pk=pk)
        except LocumAffiliations.DoesNotExist:
            return Response({'error': 'Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(membership)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            membership = self.queryset.get(pk=pk)
        except LocumAffiliations.DoesNotExist:
            return Response({'error': 'Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(membership, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            membership = self.queryset.get(pk=pk)
        except LocumAffiliations.DoesNotExist:
            return Response({'error': 'Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            membership.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class LocumMembershipsAndAffiliationsGetByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = LocumMembershipsAndAffiliationsSerializer
    queryset = LocumAffiliations.objects.all()

    def get(self, request, user_id):
        affiliations = self.queryset.filter(locum__user_id=user_id)
        if affiliations.exists():
            serializer = self.serializer_class(affiliations, many=True, read_only=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Affiliations not found'}, status=status.HTTP_400_BAD_REQUEST)


class LocumEducationalBackgroundCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumEducationalBackgroundSerializer
    queryset = LocumEducationalBackground.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocumEducationalBackgroundReadUpdateDestroyView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumEducationalBackgroundSerializer
    queryset = LocumEducationalBackground.objects.all()

    def get(self, request, pk):
        try:
            education = self.queryset.get(pk=pk)
        except LocumEducationalBackground.DoesNotExist:
            return Response({'error', 'Education not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(education)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            education = self.queryset.get(pk=pk)
        except LocumEducationalBackground.DoesNotExist:
            return Response({'error', 'Education not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(education, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            education = self.queryset.get(pk=pk)
        except LocumEducationalBackground.DoesNotExist:
            return Response({'error', 'Education not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class LocumEducationalBackgroundGetByUserIdView(GenericAPIView):
    permission_classes = []
    serializer_class = LocumEducationalBackgroundSerializer
    queryset = LocumEducationalBackground.objects.all()

    def get(self, request, user_id):
        educational = self.queryset.filter(locum__user_id=user_id)
        if educational.exists():
            serializer = self.serializer_class(educational, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error', 'Educational Background not found'}, status=status.HTTP_400_BAD_REQUEST)
