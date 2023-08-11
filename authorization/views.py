from django.contrib.auth import get_user_model, authenticate, login
from .models import User
from problems.models import Problem, ProblemSubmission
from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserUpdateSerializer, UserRegisterSerializer
from django.contrib.auth.hashers import make_password
from schoolapi.settings import GCP_PROJECT_ID, BASE_URL
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from google.oauth2 import id_token
from google.auth.transport.requests import Request


# User model used in Django
UserModel = get_user_model()

class CreateProblemSubmission(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        user = request.user
        problem_id = request.data.get('problem_id')
        answer_text = request.data.get('answer_text')
        answer_value = request.data.get('answer_value')
        solution_image = request.FILES.get('solution_pdf')

        problem = Problem.objects.get(pk=problem_id)

        submission = ProblemSubmission.objects.create(
            problem=problem,
            answer_text=answer_text,
            answer_value=answer_value,
            solution_image=solution_image
        )

        user.solved_problems.append(submission.id)
        user.save()

        return Response({'success': True, 'submission_id': submission.id}, status=status.HTTP_201_CREATED)

class PasswordResetEmailRequestView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Please enter your email'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # send confirmation email
        email_subject = 'Подтвердите свой email'
        email_body = 'Здравствуйте, {}\n\nПожалуйста, перейдите по ссылке ниже для подтверждения вашего email:\n\n{}\n'.format(
            user.username, self._get_activation_link(request, user))
        email = EmailMessage(
            email_subject, email_body, to=[user.email])
        email.send()

        return Response(status=status.HTTP_200_OK)

    def _get_activation_link(self, request, user):
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        return '{}/auth/confirm-email/{}/{}'.format(
            BASE_URL, uid, token)

class ChangePasswordViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
        
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            password = request.data.get('password')
            user.password = make_password(password)
            user.save()
            return Response({'message': 'Password changed.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if 'fields' in self.request.query_params:
            fields = self.request.query_params['fields'].split(',')
            return type('UserSerializer', (UserSerializer,), {'Meta':
                type('Meta', (object,), {'model': User, 'fields': fields})})
        return UserSerializer

class GoogleRegistrationView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            # Validate the token and get the user's Google Account ID from the decoded token.
            idinfo = id_token.verify_oauth2_token(token, Request(), GCP_PROJECT_ID)

            # Check if the user already exists in your database.
            if UserModel.objects.filter(email=idinfo['email']).exists():
                return Response({'error': 'User already exists.'}, status=status.HTTP_409_CONFLICT)

            # Create a new user if the user doesn't exist.
            user = UserModel(email=idinfo['email'])
            user.set_unusable_password()
            user.full_clean()
            user.save()

            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

        except ValueError:
            # Invalid token
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            # Validate the token and get the user's Google Account ID from the decoded token.
            idinfo = id_token.verify_oauth2_token(token, Request(), GCP_PROJECT_ID)

            # Try to authenticate the user.
            user = authenticate(request, username=idinfo['email'], password=None)

            if user:
                return Response({'token': 'Generated token for authenticated user.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        except ValueError:
            # Invalid token
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

class UserActivationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email confirmed'}, status=status.HTTP_200_OK)

        return Response({'message': 'Activation link is invalid'}, status=status.HTTP_400_BAD_REQUEST)

class ChangeEmailAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except:
            user = None
        
        print(default_token_generator.check_token(user, token))

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email changed successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email')
        password = request.data.get('password')

        print(email, password)
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        else:
            return Response({"error": "Wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # send confirmation email
        email_subject = 'Подтвердите свой email'
        email_body = 'Здравствуйте, {}\n\nПожалуйста, перейдите по ссылке ниже для подтверждения вашего email:\n\n{}\n'.format(
            user.username, self._get_activation_link(request, user))
        email = EmailMessage(
            email_subject, email_body, to=[user.email])
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_activation_link(self, request, user):
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        return '{}/auth/activate/{}/{}/'.format(
            BASE_URL, uid, token)
    
class UserUpdateAPIView(generics.UpdateAPIView):
     queryset = User.objects.all()
     serializer_class = UserUpdateSerializer
     permission_classes = (permissions.IsAuthenticated,)

     def put(self, request, *args, **kwargs):
         user = request.user

         new_email = request.data.get('email')

         if new_email and new_email != user.email:
             user.email = new_email
             user.is_active = False
             user.save()
             email_subject = 'Подтвердите свой email'
             email_body = 'Здравствуйте, {}\n\nПожалуйста, перейдите по ссылке ниже для подтверждения вашего email:\n\n{}\n'.format(
                 user.username, self._get_activation_link(request, user, new_email))
             email = EmailMessage(email_subject, email_body, to=[new_email])
             email.send()

             return Response({'message': 'Confirmation email sent'}, status=status.HTTP_200_OK)

         serializer = self.serializer_class(
             user, data=request.data, partial=True)
         serializer.is_valid(raise_exception=True)
         user = serializer.save()

         return Response(serializer.data)

     def _get_activation_link(self, request, user, new_email):
         uid = urlsafe_base64_encode(force_bytes(user.id))
         token = default_token_generator.make_token(user)
         return '{}/auth/confirm-email-user/{}/{}/'.format(
             BASE_URL, uid, token)

class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)