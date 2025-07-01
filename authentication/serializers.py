from rest_framework.serializers import ModelSerializer

from authentication.models import Worker, Employer


class EmployerSerializer(ModelSerializer):
    class Meta:
        model = Employer
        fields = 'first_name', 'last_name', 'phone_number',


class WorkerSerializer(ModelSerializer):
    class Meta:
        model = Worker
        fields = 'first_name', 'last_name', 'phone_number', 'gender', 'image', 'passport_seria', 'passport_number',
