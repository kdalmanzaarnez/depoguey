from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer

INVALID_LOGIN_MESSAGE = 'Ongeldige gebruikersnaam of wachtwoord.'


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'detail': 'CSRF-cookie gezet.'})


# DRF controleert CSRF alleen voor ingelogde gebruikers, daarom hier expliciet.
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response(
                {'detail': INVALID_LOGIN_MESSAGE},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        return Response(UserSerializer(user).data)


class MeView(APIView):

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
