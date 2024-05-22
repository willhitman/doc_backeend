from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from address.models import Address
from address.serializers import AddressSerializer
from practice.models import Practice, PracticeServices, PracticeMembershipsAndAffiliations
from practice.serializers import PracticeSerializer, PracticeServicesSerializer, PracticeUpdateSerializer, \
    PracticeUpdateAdminSerializer, PracticeMembershipsAndAffiliationsSerializer, PracticeGetSerializer


class PracticeCreateView(GenericAPIView):
    serializer_class = PracticeSerializer
    queryset = Practice.objects.all()
    permission_classes = []

    def post(self, request):
        data = {
            'user': None if request.data.get('user_id') == '' else request.data.get('user_id'),
            'national_id': None if request.data.get('national_id') == '' else request.data.get('national_id'),
            'phone_number': None if request.data.get('phone_number') == '' else request.data.get('phone_number'),
            'linkedin': None if request.data.get('linkedin') == '' else request.data.get('linkedin'),
            'title': None if request.data.get('title') == '' else request.data.get('title'),
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
        # practice_address = data.pop('address')
        serializer = self.get_serializer(data=data, partial=True)
        address_serializer = AddressSerializer(data=address, partial=True)
        if serializer.is_valid():
            saved_address = address_serializer.save()
            saved_practice = serializer.save()
            saved_practice.address = saved_address
            saved_practice.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticeReadUpdateDestroyView(GenericAPIView):
    serializer_class = PracticeUpdateSerializer
    queryset = Practice.objects.all()
    permission_classes = []

    def get(self, request, pk):
        try:
            practice = Practice.objects.get(pk=pk)
        except Practice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PracticeGetSerializer(practice)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            practice = Practice.objects.get(pk=pk)
        except Practice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        address = request.data.pop('address')

        serializer = self.serializer_class(practice, data=request.data, partial=True)

        if serializer.is_valid():
            practice_address = address
            try:
                address = Address.objects.get(pk=practice.address.pk)
            except Address.DoesNotExist:
                address = Address.objects.save(**practice_address)
                practice.address = address
                practice.save()
            else:
                address_serializer = AddressSerializer(address, practice_address)
                if address_serializer.is_valid():
                    address_serializer.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        practice = Practice.objects.get(pk=pk)
        practice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PracticeGetByUserId(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeSerializer
    queryset = Practice.objects.all()

    def get(self, request, user_id):
        try:
            practice = self.queryset.get(user_id=user_id)
        except Practice.DoesNotExist:
            return Response({'error': 'Practice not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(practice)
            return Response(serializer.data, status=status.HTTP_200_OK)


class PracticeUpdateAdmin(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeUpdateAdminSerializer
    queryset = Practice.objects.all()

    def put(self, request, pk):
        try:
            practice = self.queryset.get(pk=pk)
        except Practice.DoesNotExist:
            return Response({'error': "Practice not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:

            serializer = self.serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                # user = serializ
                pass


class PracticeServicesCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeServicesSerializer
    queryset = PracticeServices.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticeServiceReadUpdateDestroyView(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeServicesSerializer
    queryset = PracticeServices.objects.all()

    def get(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except PracticeServices.DoesNotExist:
            return Response({'error': 'Practice service not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(service)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except PracticeServices.DoesNotExist:
            return Response({'error': 'Practice service not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(service, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except PracticeServices.DoesNotExist:
            return Response({'error': 'Practice service not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PracticeServicesGetByPracticeIdViews(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeServicesSerializer
    queryset = PracticeServices.objects.all()

    def get(self, request, practice_id):
        services = self.queryset.filter(practice_id=practice_id)
        if services.exists():
            serializer = self.serializer_class(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Services not found'}, status=status.HTTP_400_BAD_REQUEST)


class PracticeMembershipAndAffiliationCreateView(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeMembershipsAndAffiliationsSerializer
    queryset = PracticeMembershipsAndAffiliations.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PracticeMembershipAndAffiliationReadUpdateDestroyView(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeMembershipsAndAffiliationsSerializer
    queryset = PracticeMembershipsAndAffiliations.objects.all()

    def get(self, request, pk):
        try:
            affiliation = self.queryset.get(pk=pk)
        except PracticeMembershipsAndAffiliations.DoesNotExist:
            return Response({'error': 'Membership or Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(affiliation)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            affiliation = self.queryset.get(pk=pk)
        except PracticeMembershipsAndAffiliations.DoesNotExist:
            return Response({'error': 'Membership or Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(affiliation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            affiliation = self.queryset.get(pk=pk)
        except PracticeMembershipsAndAffiliations.DoesNotExist:
            return Response({'error': 'Membership or Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            affiliation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PracticeMembershipAndAffiliationGetByPracticeId(GenericAPIView):
    permission_classes = []
    serializer_class = PracticeMembershipsAndAffiliationsSerializer
    queryset = PracticeMembershipsAndAffiliations.objects.all()

    def get(self, request, practice_id):
        affiliations = self.queryset.filter(practice_id=practice_id)
        if affiliations.exists():
            serializer = self.serializer_class(affiliations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Membership or Affiliation not found'}, status=status.HTTP_400_BAD_REQUEST)

