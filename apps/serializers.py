from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Category, Work, Rating
from apps.models import Region, District
from authenticate.serializers import UserSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('id',)


class DistrictSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['region'] = RegionSerializer(instance.region).data if instance.region else None
        return data


class WorkModelSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'worker', 'employer')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data if instance.category else None
        data['district'] = DistrictSerializer(instance.district).data if instance.district else None
        data['employer'] = UserSerializer(instance.employer).data if instance.employer else None
        return data


class RatingModelSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = 'stars', 'comment', 'work_id'

    def validate_price(self, value):
        if value < 0:
            raise ValidationError(_("Narx faqat raqamalardan iborat musbat son bo'lsin"))
        return value

    def validate_num_workers(self, value):
        if value < 0:
            raise ValidationError(_("Ishchilar soni faqat raqamalardan iborat musbat son bo'lsin"))

        return value
