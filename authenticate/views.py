from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from authenticate.serializers import UserSerializer


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer})
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer


