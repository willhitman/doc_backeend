from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from django.db.models import Q
from Doctor.models import Doctor, DoctorSpecialization, DoctorLanguages, DoctorAffiliationsAndMemberships, \
    DoctorEducationalBackground, Insurance
from Doctor.serializers import DoctorSerializer, DoctorSpecializationSerializer, DoctorLanguagesSerializer, \
    DoctorGetSerializer, DoctorAffiliationSerializer, DoctorEducationalBackgroundSerializer, \
    ServicesSerializer, DoctorSearchByNameSerializer,  DoctorCreateSerializer, \
    DoctorUpdateSerializer
from accounts.models import User
from accounts.serializers import DoctorInsuranceSerializer, UserSerializer
from accounts.service_account_manager import save_user_service_accounts
from address.models import Address, Services
from address.serializers import AddressSerializer


# Doctor ##################################################################################################

class CreateDoctorView(CreateAPIView):
    serializer_class = DoctorCreateSerializer

    def post(self, request, *args, **kwargs):
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

        serializer = self.serializer_class(data=data, partial=True)
        address_serializer = AddressSerializer(data = address, partial=True)
        if serializer.is_valid():
            saved_doctor = serializer.save()
            if address_serializer.is_valid():
                saved_address = address_serializer.save()
                saved_doctor.address = saved_address
            saved_doctor.save()
            # create service account reference
            save_user_service_accounts(saved_doctor.user, Doctor, saved_doctor.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorUpdateDestroyGet(GenericAPIView):
    serializer_class = DoctorUpdateSerializer
    queryset = Doctor.objects.all()
    permission_classes = []

    def put(self, request, pk):
        try:
            doctor = self.queryset.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                'user': {
                    'first_name': None if request.data.get('first_name') == '' else request.data.get('first_name'),
                    'last_name': None if request.data.get('last_name') == '' else request.data.get('last_name'),
                    'username': None if request.data.get('email') == '' else request.data.get('email'),
                    'role': 'Doctor',
                    'gender': None if request.data.get('gender') == '' else request.data.get('gender'),
                    'email': None if request.data.get('email') == '' else request.data.get('email'),
                },

                'national_id': None if request.data.get('national_id') == '' else request.data.get('national_id'),
                'phone_number': None if request.data.get('phone_number') == '' else request.data.get('phone_number'),
                'linkedin': None if request.data.get('linkedin') == '' else request.data.get('linkedin'),
                'title': None if request.data.get('title') == '' else request.data.get('title'),
                'profile_picture': None if request.data.get('profile_picture') == '' else request.data.get(
                    'profile_picture'),
                'languages': None if request.data.get('languages') == '' else request.data.get('languages'),
                'address': {
                    'door_address': None if request.data.get('door_address') == '' else request.data.get(
                        'door_address'),
                    'street_one': None if request.data.get('street_one') == '' else request.data.get('street_one'),
                    'street_two': None if request.data.get('street_two') == '' else request.data.get('street_two'),
                    'suburb': None if request.data.get('suburb') == '' else request.data.get('suburb'),
                    'province': None if request.data.get('province') == '' else request.data.get('province'),
                    'city': None if request.data.get('city') == '' else request.data.get('city'),
                }

            }
            print(data)

            serializer = DoctorSerializer(doctor, data=data, partial=True)
            user_data = data.pop('user')
            try:
                user = User.objects.get(pk=doctor.user.pk)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_serializer = UserSerializer(user, data=user_data, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()

                if serializer.is_valid():
                    doc_address = serializer.validated_data.pop('address')
                    saved = serializer.save()
                    if doctor.address:
                        try:
                            address = Address.objects.get(pk=doctor.address.pk)
                        except Address.DoesNotExist:
                            saved_address = Address.objects.create(**doc_address)
                            saved.address = saved_address
                            saved.save()
                        else:
                            address_serializer = AddressSerializer(address, data=doc_address, partial=True)
                            if address_serializer.is_valid():
                                address_serializer.save()
                    else:
                        saved_address = Address.objects.create(**doc_address)
                        saved.address = saved_address
                        saved.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            doctor = self.queryset.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = DoctorGetSerializer(doctor)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            doctor = self.queryset.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            doctor.delete()
            return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Specialization Starts here ####################################################

class DoctorSpecializationCreate(GenericAPIView):
    serializer_class = DoctorSpecializationSerializer
    queryset = DoctorSpecialization.objects.all
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def update_staff_personal_document(request, user_id):
    if request.method == 'POST':
        try:
            personal_doc = DoctorSpecialization.objects.get(doctor__user_id=user_id)
        except DoctorSpecialization.DoesNotExist:
            return Response(data={'error': 'Doctor Specialization record not Found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                cert = request.FILES['file']
            except KeyError:
                return Response(data={'error': 'Doctor Specialization Document missing.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                cert.name = f'{personal_doc.doctor.pk}{personal_doc.doctor.user.last_name}.{cert.name.split(".")[1]}'
                personal_doc.file = cert
                personal_doc.save()
                return Response(data={'message': 'Doctor Specialization document updated successfully.'},
                                status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([])
def update_doc_avatar(request, user_id):
    if request.method == 'POST':
        try:
            doc = Doctor.objects.get(user_id=user_id)
        except Doctor.DoesNotExist:
            return Response(data={'error': 'Doctor record not Found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                avatar = request.FILES['avatar']
            except KeyError:
                return Response(data={'error': 'Document missing.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                avatar.name = f'{doc.pk}{doc.user.last_name}.{avatar.name.split(".")[1]}'
                doc.profile_picture = avatar
                doc.save()
                return Response(data={'message': 'Doctor document updated successfully.'},
                                status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class DoctorGetByUserId(GenericAPIView):
    serializer_class = DoctorGetSerializer
    queryset = Doctor.objects.all()
    permission_classes = []

    def get(self, request, pk):
        try:
            doctor = self.queryset.get(user_id=pk)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(doctor)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class DoctorSpecializationUpdateDestroyGEt(GenericAPIView):
    serializer_class = DoctorSpecializationSerializer
    queryset = DoctorSpecialization.objects.all()
    permission_classes = []

    def put(self, request, pk):
        try:
            specialization = self.queryset.get(pk=pk)
        except DoctorSpecialization.DoesNotExist:
            return Response({'error': 'Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(specialization, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            specialization = self.queryset.get(pk=pk)
        except DoctorSpecialization.DoesNotExist:
            return Response({'error': 'Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(specialization)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            specialization = self.queryset.get(pk=pk)
        except DoctorSpecialization.DoesNotExist:
            return Response({'error': 'Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            specialization.delete()
            return Response({'message': 'Specialization Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)


class DoctorSpecializationGetByUserId(GenericAPIView):
    serializer_class = DoctorSpecializationSerializer
    queryset = DoctorSpecialization.objects.all()
    permission_classes = []

    def get(self, request, pk):
        specialization = self.queryset.filter(doctor__user_id=pk)
        if specialization.exists():
            serializer = self.serializer_class(specialization, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Doctor Specialization not found'}, status=status.HTTP_400_BAD_REQUEST)


class DoctorLanguagesCreate(GenericAPIView):
    serializer_class = DoctorLanguagesSerializer
    queryset = DoctorLanguages.objects.all
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorLanguagesGet(GenericAPIView):
    serializer_class = DoctorLanguagesSerializer
    queryset = DoctorLanguages.objects.all()
    permission_classes = []

    def get(self, request):
        languages = self.queryset.all()
        serializer = DoctorLanguagesSerializer(languages, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DoctorAffiliationCreate(GenericAPIView):
    serializer_class = DoctorAffiliationSerializer
    queryset = DoctorAffiliationsAndMemberships
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorAffiliationUpdateDestroyView(GenericAPIView):
    serializer_class = DoctorAffiliationSerializer
    queryset = DoctorAffiliationsAndMemberships.objects.all()
    permission_classes = []

    def get(self, request, pk):
        try:
            doctor_affiliation = self.queryset.get(pk=pk)
        except DoctorAffiliationsAndMemberships.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(doctor_affiliation)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            doctor_affiliation = self.queryset.get(pk=pk)
        except DoctorAffiliationsAndMemberships.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(doctor_affiliation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            doctor_affiliation = self.queryset.get(pk=pk)
        except DoctorAffiliationsAndMemberships.DoesNotExist:
            return Response({'error': 'Record not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            doctor_affiliation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorAffiliationGetByUserIdView(GenericAPIView):
    serializer_class = DoctorAffiliationSerializer
    queryset = DoctorAffiliationsAndMemberships.objects.all()
    permission_classes = []

    def get(self, request, userId):
        affiliations = self.queryset.filter(doctor__user_id=userId)
        if affiliations.exists():
            serializer = self.serializer_class(affiliations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Affiliations not found'}, status=status.HTTP_400_BAD_REQUEST)


class DoctorEducationalBackgroundCreate(GenericAPIView):
    serializer_class = DoctorEducationalBackgroundSerializer
    queryset = DoctorEducationalBackground.objects.all()
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorEducationalBackgroundUpdateDestroyView(GenericAPIView):
    serializer_class = DoctorEducationalBackgroundSerializer
    queryset = DoctorEducationalBackground.objects.all()
    permission_classes = []

    def put(self, request, pk):
        try:
            doctor_education = self.queryset.get(pk=pk)
        except DoctorEducationalBackground.DoesNotExist:
            return Response({'error': 'Doctor Education not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(doctor_education, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            doctor_education = self.queryset.get(pk=pk)
        except DoctorEducationalBackground.DoesNotExist:
            return Response({'error': 'Doctor Education not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(doctor_education, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            doctor_education = self.queryset.get(pk=pk)
        except DoctorEducationalBackground.DoesNotExist:
            return Response({'error': 'Doctor Education not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            doctor_education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorEducationalBackgroundGetByUserId(GenericAPIView):
    serializer_class = DoctorEducationalBackgroundSerializer
    queryset = DoctorEducationalBackground.objects.all()
    permission_classes = []

    def get(self, request, userId):
        educations = self.queryset.filter(doctor__user_id=userId)
        if educations.exists():
            serializer = self.serializer_class(educations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Educations not found'}, status=status.HTTP_400_BAD_REQUEST)


# class DoctorPracticeLocationInfoCreate(GenericAPIView):
#     serializer_class = DoctorPracticeLocationInfoSerializer
#     queryset = DoctorPracticeLocationInfo.objects.all()
#     permission_classes = []
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class DoctorPracticeLocationInforUpdateDestroyView(GenericAPIView):
#     serializer_class = DoctorPracticeLocationInfoSerializer
#     queryset = DoctorPracticeLocationInfo.objects.all()
#     permission_classes = []
#
#     def put(self, request, pk):
#         try:
#             practice_location = self.queryset.get(pk=pk)
#         except DoctorPracticeLocationInfo.DoesNotExist:
#             return Response({'error': 'Practice Location not found'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer = self.serializer_class(practice_location, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request, pk):
#         try:
#             practice_location = self.queryset.get(pk=pk)
#         except DoctorPracticeLocationInfo.DoesNotExist:
#             return Response({'error': 'Practice Location not found'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer = self.serializer_class(practice_location)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk):
#         try:
#             practice_location = self.queryset.get(pk=pk)
#         except DoctorPracticeLocationInfo.DoesNotExist:
#             return Response({'error': 'Practice Location not found'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             practice_location.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class DoctorPracticeLocationInfoGetByUserId(GenericAPIView):
#     serializer_class = DoctorPracticeLocationInfoSerializer
#     queryset = DoctorPracticeLocationInfo.objects.all()
#     permission_classes = []
#
#     def get(self, request, userId):
#         practice_locations = self.queryset.filter(doctor__user_id=userId)
#         if practice_locations.exists():
#             serializer = self.serializer_class(practice_locations, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({'error': 'Practice Locations not found'}, status=status.HTTP_400_BAD_REQUEST)


class DoctorServicesCreate(GenericAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorServicesUpdateDestroyView(GenericAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = []

    def put(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except Services.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(service, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except Services.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(service)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            service = self.queryset.get(pk=pk)
        except Services.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorServicesGetAll(GenericAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = []

    def get(self, request):
        services = self.queryset.all()
        if services.exists():
            serializer = self.serializer_class(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Services not found'}, status=status.HTTP_400_BAD_REQUEST)


class DoctorServicesGetAllByUserId(GenericAPIView):
    serializer_class = ServicesSerializer
    queryset = Services.objects.all()
    permission_classes = []

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return Response({'error':'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            services= self.queryset.filter(user_id=user_id)


class DoctorInsuranceCreate(GenericAPIView):
    serializer_class = DoctorInsuranceSerializer
    queryset = Insurance.objects.all()
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorInsuranceUpdateDestroyView(GenericAPIView):
    serializer_class = DoctorInsuranceSerializer
    queryset = Insurance.objects.all()
    permission_classes = []

    def put(self, request, pk):
        try:
            insurance = self.queryset.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({'error': 'Insurance not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(insurance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            insurance = self.queryset.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({'error': 'Insurance not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(insurance)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            insurance = self.queryset.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({'error': 'Insurance not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            insurance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorInsuranceGetByDoctor(GenericAPIView):
    serializer_class = DoctorInsuranceSerializer
    queryset = Insurance.objects.all()
    permission_classes = []

    def get(self, request):
        insurances = self.queryset.all()
        if insurances.exists():
            serializer = self.serializer_class(insurances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Insurances not found'}, status=status.HTTP_400_BAD_REQUEST)



