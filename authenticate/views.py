from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView

from authenticate.models import User, WorkerAdditional
from authenticate.permissions import WorkerPermission
from authenticate.serializers import UserSerializer, WorkerAdditionalSerializer, UserUpdateSerializer, \
    ChangePasswordSerializer


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(tags=['user'], request=UserSerializer, responses={200: UserSerializer})
class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['user'], request=ChangePasswordSerializer, responses={200: ChangePasswordSerializer})
class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['user-additional'], request=WorkerAdditionalSerializer,
               responses={200: WorkerAdditionalSerializer})
class WorkerAdditionalCreateAPIView(CreateAPIView):
    serializer_class = WorkerAdditionalSerializer
    queryset = WorkerAdditional.objects.all()
    permission_classes = [WorkerPermission]
