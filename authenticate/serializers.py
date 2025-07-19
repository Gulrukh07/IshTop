import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer, Serializer

from authenticate.models import WorkerAdditional, User, Region


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = 'id',


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'password', 'avatar', 'role',
        read_only_fields = 'id',

    def validate_phone_number(self, value):
        phone = re.sub('\D', '', value)
        pattern = r'^998(90|91|93|94|95|97|98|99|33|88|50)\d{7}$'

        if not re.match(pattern, phone):
            raise ValidationError('Telefon raqami quyidagi formatda bo‘lishi kerak: +998XXXXXXXXX')

        queryset = User.objects.filter(phone_number=phone)
        if queryset.exists():
            raise ValidationError('Bu telefon raqamli foydalanuvchi allaqachon mavjud.')
        return phone

    def validate_password(self, value):
        if len(value) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
        if len(value) > 20:
            raise ValidationError('Password must be at most 20 characters long.')
        if not re.search(r'\d', value):
            raise ValidationError('Password must contain at least one digit.')
        if not re.search(r'[A-Za-z]', value):
            raise ValidationError('Password must contain at least one letter.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError('Password must contain at least one special character.')

        return value

    def validate_avatar(self, value):
        if value and not value.name.lower().endswith(('.jpg', 'jpeg', 'png')):
            raise ValidationError('Avatar must be an image.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'avatar',

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(Serializer):
    old_password = CharField(write_only=True, required=True)
    new_password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)


class WorkerAdditionalSerializer(ModelSerializer):
    class Meta:
        model = WorkerAdditional
        fields = 'gender', 'passport_seria', 'passport_number', 'region', 'user',

    def validate_passport_seria(self, value):
        pattern = r'^(AA|AB|AC|AD)$'
        if not re.match(pattern, value):
            raise ValidationError('Invalid passport seria.')

    def validate_passport_number(self, value):
        pattern = r'^\d{7}$'
        if not re.match(pattern, value):
            raise ValidationError('Invalid passport number.')
