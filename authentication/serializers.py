from rest_framework.serializers import ModelSerializer

from models import Employer, Worker


class UserSerializer(ModelSerializer):
    class Meta:
        model = Employer
        fields = 'first_name', 'last_name', 'phone_number', 'password', 'avatar', 'role',


class WorkerAdditionalSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = 'gender', 'image', 'passport_seria', 'passport_number', 'region_id',
