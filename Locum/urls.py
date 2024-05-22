from django.urls import path

from Locum import views

urlpatterns = [
    path('', views.LocumCreateView.as_view()),
    path('<int:pk>/', views.LocumReadUpdateDestroyView.as_view()),
    path('get-by-user-id/<int:user_id>/', views.LocumGetByUserIdView.as_view(), name='get-by-user-id'),
    path('locum-specialization/', views.LocumSpecializationCreateView.as_view()),
    path('locum-specialization/<int:pk>/', views.LocumSpecializationReadUpdateDestroyView.as_view()),
    path('locum-specialization/get-by-user-id/<int:pk>/', views.LocumSpecializationGetByUserIdView.as_view()),
    path('locum-memberships-and-affiliations/', views.LocumMembershipsAndAffiliationsCreateView.as_view()),
    path('locum-memberships-and-affiliations/<int:pk>/',
         views.LocumMembershipsAndAffiliationsReadUpdateDestroyView.as_view()),
    path('locum-memberships-and-affiliations/get-by-user-id/<int:user_id>/',
         views.LocumMembershipsAndAffiliationsGetByUserId.as_view()),

    path('locum-educational-background/', views.LocumEducationalBackgroundCreateView.as_view()),
    path('locum-educational-background/<int:pk>/', views.LocumEducationalBackgroundReadUpdateDestroyView.as_view()),
    path('locum-educational-background/get-by-user-id/<int:user_id>/',
         views.LocumEducationalBackgroundGetByUserIdView.as_view()),

]