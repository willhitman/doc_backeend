from django.urls import path

from address.insurances import views

urlpatterns=[
    path('get-all-insurances/', views.InsuranceGetAll.as_view())
]