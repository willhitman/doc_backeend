from django.urls import path

from practice import views

urlpatterns = [
    path('', views.PracticeCreateView.as_view()),
    path('<int:pk>/', views.PracticeReadUpdateDestroyView.as_view()),
    path('get-by-user-id/<int:user_id>/', views.PracticeGetByUserId.as_view()),
    path('practice-services/', views.PracticeServicesCreateView.as_view()),

    path('get-by-practice-id/<int:practice_id>/', views.PracticeServicesGetByPracticeIdViews.as_view()),

    path('practice-memberships-and-affiliations/', views.PracticeMembershipAndAffiliationCreateView.as_view()),
    path('practice-memberships-and-affiliations/<int:pk>/',
         views.PracticeMembershipAndAffiliationReadUpdateDestroyView.as_view()),
    path('practice-memberships-and-affiliations/get-by-practice-id/<int:practice_id>/',
         views.PracticeMembershipAndAffiliationGetByPracticeId.as_view()),
]
