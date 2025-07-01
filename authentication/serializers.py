from rest_framework.serializers import ModelSerializer

from authentication.models import WorkerAdditional, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'password', 'role', 'avatar'


class WorkerAdditionalSerializer(ModelSerializer):
    class Meta:
        model = WorkerAdditional
        fields = 'gender', 'passport_seria', 'passport_number', 'user_id', 'region_id',
