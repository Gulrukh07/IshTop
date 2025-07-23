from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView

from authenticate.models import User
from authenticate.serializers import UserSerializer, WorkerAdditionalSerializer


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(tags=['user'], request=WorkerAdditionalSerializer, responses={200: WorkerAdditionalSerializer})
class WorkerAdditionalCreateAPIView(CreateAPIView):
    serializer_class = WorkerAdditionalSerializer

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()