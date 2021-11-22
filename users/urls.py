from django.urls import path, include
from .views import UserDetail, ObtainAuthTokenView,registration_view
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('info/<str:pk>/', UserDetail.as_view(), name='user-info'),
    # path('register', RegistrationView.as_view(), name="register"),
    path('login', ObtainAuthTokenView.as_view(), name="login"),
    path('register', registration_view, name="register"),
]
