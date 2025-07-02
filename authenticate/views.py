from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.generics import CreateAPIView

from authenticate.serializers import UserSerializer


@extend_schema(tags=['user'], request=UserSerializer, responses={201: UserSerializer},
               examples=[OpenApiExample('Example User Creation', value={
                   'fullname': 'John Doe',
                   'phone': '1276358167',
                   'avatar': 'example.jpg'
               }, request_only=True)])
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
