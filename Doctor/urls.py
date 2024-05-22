from django.urls import path

from Doctor import views

urlpatterns = [
    path('', views.CreateDoctorView.as_view()),
    path('<int:pk>/', views.DoctorUpdateDestroyGet.as_view()),
    path('specialization/', views.DoctorSpecializationCreate.as_view()),
    path('specialization/<int:pk>/', views.DoctorSpecializationUpdateDestroyGEt.as_view()),
    path('doctors-languages/', views.DoctorLanguagesCreate.as_view()),
    path('doctors-languages-get-all/', views.DoctorLanguagesGet.as_view()),
    path('doctor/get-by-user-id/<int:pk>/', views.DoctorGetByUserId.as_view()),
    path('doctor/change-avatar/<int:user_id>/', views.update_doc_avatar),
    path('doctor/upload-specialization-document/<int:user_id>/', views.update_staff_personal_document),
    path('doctor/specialization/get-by-user-id/<int:pk>/', views.DoctorSpecializationGetByUserId.as_view()),
    path('doctor/affiliation/', views.DoctorAffiliationCreate.as_view()),
    path('doctor/affiliation/<int:pk>/', views.DoctorAffiliationUpdateDestroyView.as_view()),
    path('doctor/affiliation/get-all-by-doctor-uder-id/<int:userId>/',
         views.DoctorAffiliationGetByUserIdView.as_view()),
    path('doctor/educational-background/', views.DoctorEducationalBackgroundCreate.as_view()),
    path('doctor/educational-background/<int:pk>/', views.DoctorEducationalBackgroundUpdateDestroyView.as_view()),
    path('doctor/educational-background/get-all-by-doctor-user-id/<int:userId>/', views.
         DoctorEducationalBackgroundGetByUserId.as_view()),

    path('doctor/services/', views.DoctorServicesCreate.as_view()),
    path('doctor/services/<int:pk>/', views.DoctorServicesUpdateDestroyView.as_view()),
    path('doctor/services/get-all/', views.DoctorServicesGetAll.as_view()),
    path('doctor/insurance/', views.DoctorInsuranceCreate.as_view()),
    path('doctor/insurance/<int:pk>/', views.DoctorInsuranceUpdateDestroyView.as_view()),
    path('doctor/insurance/get-all/',
         views.DoctorInsuranceGetByDoctor.as_view()),

]
