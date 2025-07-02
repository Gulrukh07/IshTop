import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from authenticate.models import WorkerAdditional, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'password', 'role', 'avatar'

        def validate_phone_number(self, value):
            pattern = r'^\+?\d{12,15}$'
            if not re.match(pattern, value):
                raise ValidationError('Phone number must be entered in the format: +999999999999')

            queryset = User.objects.filter(phone_number=value)
            if queryset.exists():
                raise ValidationError('User already exists')
            return value


class WorkerAdditionalSerializer(ModelSerializer):
    class Meta:
        model = WorkerAdditional
        fields = 'gender', 'passport_seria', 'passport_number', 'user_id', 'region_id',
