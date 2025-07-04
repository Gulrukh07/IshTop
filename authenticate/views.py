from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from authenticate.serializers import UserSerializer, WorkerAdditionalSerializer


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer


@extend_schema(tags=['user'], request=WorkerAdditionalSerializer, responses={200: WorkerAdditionalSerializer})
class WorkerAdditionalCreateAPIView(CreateAPIView):
    serializer_class = WorkerAdditionalSerializer