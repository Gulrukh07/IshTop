from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from apps.models import Work, Category, Region, District
from authenticate.serializers import UserSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class RegionModelSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('id',)


class DistrictModelSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['region'] = RegionModelSerializer(instance.region).data if instance.region else None
        return data


class WorkModelSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'worker', 'employer',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data if instance.category else None
        data['district'] = DistrictSerializer(instance.district).data if instance.district else None
        data['employer'] = UserSerializer(instance.employer).data if instance.employer else None
        return data

    def validate_price(self, value):
        if value < 0:
            raise ValidationError(_("Narx faqat raqamalardan iborat musbat son bo'lsin"))
        return value

    def validate_num_workers(self, value):
        if value < 0:
            raise ValidationError(_("Ishchilar soni faqat raqamalardan iborat musbat son bo'lsin"))

        return value


class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = 'name', 'status', 'num_workers', 'description', 'category', 'latitude', 'longitude', 'district', 'price'
        read_only_fields = ('id', 'status')

    district = PrimaryKeyRelatedField(queryset=District.objects.all(), required=True)
    category = PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data if instance.category else None
        data['district'] = DistrictSerializer(instance.district).data if instance.district else None
        return data
