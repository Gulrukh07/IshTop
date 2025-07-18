import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from authenticate.models import WorkerAdditional, User, Region


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('id',)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'password', 'avatar', 'role',
        read_only_fields = 'id',

    def validate_phone_number(self, value):
        phone_number = re.sub(r'\D', '', value)
        pattern = r'^998(90|91|93|94|95|97|98|99|33|88)\d{7}$'
        if not re.match(pattern, phone_number):
            raise ValidationError('Phone number must be entered in the format: +999999999999')

        queryset = User.objects.filter(phone_number=phone_number)
        if queryset.exists():
            raise ValidationError('User already exists.')

        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError('Password must be at least 6 characters long.')
        if len(value) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError('Password must contain at least one special character.')

        return value
    def create(self, validated_data):
        user = User(phone_number=validated_data['phone_number'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class WorkerAdditionalSerializer(ModelSerializer):
    class Meta:
        model = WorkerAdditional
        fields = 'gender', 'passport_seria', 'passport_number', 'user_id', 'region_id',

    def validate_passport_seria(self, value):
        pattern = r'^(AA|AB|AC|AD)$'
        if not re.match(pattern, value):
            raise ValidationError('Invalid passport seria.')

    def validate_passport_number(self, value):
        pattern = r'^\d{7}$'
        if not re.match(pattern, value):
            raise ValidationError('Invalid passport number.')

