from django.contrib.auth import get_user_model
from django.utils import timezone
from .serializers import RegisterSerializer
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class IssueVerficationCodeView(views.APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        user = User.objects.get(email=email)
        if not user:
            return Response({"status": "failed", "message": "user-not-found"})
        if not user.new_verification_code_allowed:
            return Response({"status": "failed", "message": "too-many-request"})

        sent = user.verification_code_generator()
        if sent:
            return Response({"status": "success", "code": user.verification_code})

        return Response({"status": "failed", "message": "something-went-wrong"})


class VerifyEmailWithCode(views.APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code", None)
        email = request.data.get("email", None)
        user = User.objects.get(email=email)
        if not user:
            return Response({"status": "failed", "message": "user-not-found"})

        if code == str(user.verification_code):
            if timezone.now() <= user.code_expiration:
                user.is_active = True
                user.activation_date = timezone.now()
                user.save()
                return Response({"status": "success", "message": "user-activated"})
            else:
                return Response({"status": "failed", "message": "code-expired"})

        else:
            return Response({"status": "failed", "message": "code-wrong"})
