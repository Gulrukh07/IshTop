from rest_framework.serializers import ModelSerializer

from apps.models import Category, Work, Rating


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'name',


class WorkModelSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = 'name', 'category_id', 'region_id', 'latitude', 'longitude', 'price', 'description', 'num_workers', 'employer_id', 'worker_id', 'status',


class RatingModelSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = 'stars', 'comment', 'work_id'


