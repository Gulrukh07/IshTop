from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView

from authenticate.models import User, WorkerAdditional
from authenticate.permissions import WorkerPermission
from authenticate.serializers import UserSerializer, WorkerAdditionalSerializer, UserUpdateSerializer, \
    ChangePasswordSerializer, WorkerAdditionalUpdateSerializer


@extend_schema(tags=['user'])
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()


@extend_schema(tags=['user'])
class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['user'])
class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


@extend_schema(tags=['user'])
class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['user'])
class UserDeleteAPIView(APIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['change-passwd'])
class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['user-additional'])
class WorkerAdditionalCreateAPIView(CreateAPIView):
    serializer_class = WorkerAdditionalSerializer
    queryset = WorkerAdditional.objects.all()
    permission_classes = [WorkerPermission]


@extend_schema(tags=['user-additional'])
class WorkerAdditionalUpdateAPIView(UpdateAPIView):
    serializer_class = WorkerAdditionalUpdateSerializer
    queryset = WorkerAdditional.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
