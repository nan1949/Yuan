from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RegistrationSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import (generics, mixins)
from rest_framework.authtoken.models import Token


# class RegistrationView(generics.GenericAPIView,
#                        mixins.CreateModelMixin):
#     # permission_classes = [
#     #     # IsAuthenticatedOrReadOnly,
#     #     # IsOwnerOrReadOnly,
#     #     IsAuthenticated
#     # ]
#     # authentication_classes = (TokenAuthentication,)
#
#     serializer_class = RegistrationSerializer
#
#     def post(self, request):
#         return self.create(request)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        if validate_email(email) is not None:
            data['error_message'] = 'That email is already in use.'
            data['response'] = 'Error'
            return Response(data)

        username = request.data.get('username', '0')
        if validate_username(username) is not None:
            data['error_message'] = 'That username is already in use.'
            data['response'] = 'Error'
            return Response(data)

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['pk'] = user.pk
            token = Token.objects.get(user=user).key
            data['token'] = token
            # data['mod'] = user.is_moderator
            if (user.is_moderator):
                data['mod'] = "true"
            else:
                data['mod'] = "false"
        else:
            data = serializer.errors
        return Response(data)


def validate_email(email):
    user = None
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    if user is not None:
        return email


def validate_username(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    if user != None:
        return username


class UserDetail(generics.GenericAPIView,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)


class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = user.pk
            context['email'] = email.lower()
            context['token'] = token.key
            context['username'] = user.username
            if (user.is_moderator):
                context['mod'] = "true"
            else:
                context['mod'] = "false"
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'

        return Response(context)
