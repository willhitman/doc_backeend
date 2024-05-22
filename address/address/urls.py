from django.urls import path

from address.address import views

urlpatterns = [
    path('', views.AddressCreateView.as_view()),
    path('<int:pk>/', views.AddressReadUpdateDestroyView.as_view()),
]