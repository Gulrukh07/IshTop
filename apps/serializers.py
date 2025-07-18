from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.models import Work, Category
from authenticate.models import Region
from authenticate.serializers import RegionSerializer
from apps.models import Category, Work, Rating


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)



class WorkModelSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = ('id','created_at','updated_at','status', 'worker', 'employer', "category")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data
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
