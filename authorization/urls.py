from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationAPIView.as_view()),
    path('activate/<str:uidb64>/<str:token>/', views.UserActivationAPIView.as_view(), name='activate'),

    path('login/', views.UserLoginAPIView.as_view()),

    path('update/', views.UserUpdateAPIView.as_view()),
    path('confirm-email-user/<str:uidb64>/<str:token>/', views.ChangeEmailAPIView.as_view()),

    path('delete/', views.UserDeleteAPIView.as_view()),

    path('register-with-google/', views.GoogleRegistrationView.as_view()),
    path('login-with-google/', views.GoogleLoginView.as_view()),

    path('reset-password/', views.PasswordResetEmailRequestView.as_view()),

    path('confirm-email/<str:uidb64>/<str:token>/', views.ChangePasswordViewSet.as_view()),

    path('create-problem-submission/', views.CreateProblemSubmission.as_view())
]