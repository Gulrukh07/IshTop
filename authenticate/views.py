from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticate.models import User, WorkerAdditional
from authenticate.permissions import WorkerPermission
from authenticate.serializers import UserSerializer, WorkerAdditionalSerializer, UserUpdateSerializer, \
    ChangePasswordSerializer, WorkerAdditionalUpdateSerializer, VerifyOTPSerializer, SendOTPSerializer
from authenticate.services.otp_services import OtpService


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['user'], request=UserUpdateSerializer, responses={200: UserSerializer})
class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['user'], request=ChangePasswordSerializer, responses={200: ChangePasswordSerializer})
class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['user-additional'], request=WorkerAdditionalSerializer,
               responses={200: WorkerAdditionalSerializer})
class WorkerAdditionalCreateAPIView(CreateAPIView):
    serializer_class = WorkerAdditionalSerializer
    queryset = WorkerAdditional.objects.all()
    permission_classes = [WorkerPermission]


@extend_schema(tags=['user-additional'], request=WorkerAdditionalUpdateSerializer,
               responses={200: WorkerAdditionalSerializer})
class WorkerAdditionalUpdateAPIView(UpdateAPIView):
    serializer_class = WorkerAdditionalUpdateSerializer
    queryset = WorkerAdditional.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

otp_service = OtpService()

class SendOTPView(APIView):
    serializer_class = SendOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        code = otp_service.generate_code()
        sent = otp_service.send_otp(phone, code)

        if not sent:
            return Response({"detail": "Failed to send OTP."}, status=500)
        return Response({"detail": "OTP sent successfully."})


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]

        verified = otp_service.verify_otp(phone, code)
        if not verified:
            return Response({"detail": "Invalid or expired OTP."}, status=400)
        return Response({"detail": "Phone number verified successfully."})
