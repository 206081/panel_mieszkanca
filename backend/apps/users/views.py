from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.serializers import TokenAccessObtainSerializer, UserSerializer, UserWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if "password" in self.request.data:
            user.set_password(self.request.data.get("password"))
            user.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(methods=["GET"], detail=False)
    def profile(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        last_name = request.data.get("last_name", "last")
        first_name = request.data.get("first_name", "first")
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if User.objects.filter(email__iexact=email).exists():
            return Response({"status": 210})

        # user creation
        user = User.objects.create_user(
            email=email,
            password=password,
            last_name=last_name,
            first_name=first_name,
            is_admin=False,
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False)
    def password_reset(self, request, format=None):
        if User.objects.filter(email=request.data["email"]).exists():
            user = User.objects.get(email=request.data["email"])
            params = {"user": user, "DOMAIN": settings.DOMAIN}
            try:
                send_mail(
                    subject="Password reset",
                    message=render_to_string("mail/password_reset.txt", params),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.data["email"]],
                )
            except OSError:
                print("Email sent.")
            return Response(status=status.HTTP_200_OK, data=render_to_string("mail/password_reset.txt", params))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], detail=False)
    def password_change(self, request, format=None):
        if User.objects.filter(id=self.request.user.id).exists():
            print("User exist")
            user = User.objects.get(id=self.request.user.id)
            user.set_password(request.data["password"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print("User does not exist")
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutViewSet(APIView):
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        if self.request.data.get("all"):
            for token in OutstandingToken.objects.filter(user=request.user):
                BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "All Tokens Blacklisted."})
        refresh_token = self.request.data.get("refresh")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "Token Blacklisted."})


class TokenAccessObtain(TokenObtainPairView):
    serializer_class = TokenAccessObtainSerializer
