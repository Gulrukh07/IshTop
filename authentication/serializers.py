from rest_framework.serializers import ModelSerializer


class Employer(ModelSerializer):
    class Meta:
        model = Employer
        fields = 'first_name', 'last_name', 'phone_number',


class Worker(ModelSerializer):
    class Meta:
        model = Worker
        fields = 'first_name', 'last_name', 'phone_number', 'gender', 'image', 'passport_seria', 'passport_number',
