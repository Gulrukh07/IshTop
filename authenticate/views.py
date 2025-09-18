from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from authenticate.models import User, WorkerAdditional
from authenticate.permissions import WorkerPermission
from authenticate.serializers import UserModelSerializer, WorkerAdditionalSerializer, UserUpdateSerializer, \
    ChangePasswordSerializer, WorkerAdditionalUpdateSerializer


########################################### USER ###########################################
@extend_schema(tags=['user'])
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserModelSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()


@extend_schema(tags=['user'])
class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserModelSerializer
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
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema(tags=['user'])
class UserDeleteAPIView(DestroyAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


########################################### PASSWORD ###########################################
@extend_schema(tags=['change-passwd'])
class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


########################################### USER-ADDITIONAL ###########################################
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
