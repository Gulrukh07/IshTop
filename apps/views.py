from drf_spectacular.utils import extend_schema
<<<<<<< HEAD
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
=======
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
>>>>>>> b3b3e91 (updated)

from apps.models import Work, Region, District, Rating, RatingImages
from apps.permissions import CustomerPermission
from apps.serializers import WorkModelSerializer, DistrictSerializer, WorkSerializer, \
    RegionModelSerializer, RatingModelSerializer, RatingUpdateSerializer, RatingImagesModelSerializer


@extend_schema(tags=['Work'])
class WorkCreateApi(CreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkModelSerializer
    permission_classes = [CustomerPermission]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


@extend_schema(tags=['Work'])
class LatestWorkListApi(ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkModelSerializer

    def get_queryset(self):
        query = super().get_queryset().filter(worker=None).order_by('-created_at')
        return query


@extend_schema(tags=['Work'])
class EmployerWorksListApi(ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkModelSerializer

    def get_queryset(self):
        employer_id = self.kwargs.get('employer_id')
        return super().get_queryset().filter(employer=employer_id).order_by('-created_at')


@extend_schema(tags=['Work'])
class WorkerWorksListApi(ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkModelSerializer

    def get_queryset(self):
        worker_id = self.kwargs.get('worker_id')
        return super().get_queryset().filter(worker=worker_id).order_by('-created_at')


@extend_schema(tags=['Work'])
class WorkUpdateApi(UpdateAPIView):
    permission_classes = [CustomerPermission]
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


@extend_schema(tags=['Region'])
class RegionListAPiView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionModelSerializer


@extend_schema(tags=['District'])
class DistrictListAPiView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get_queryset(self):
        query = super().get_queryset()
        region = self.kwargs.get('region_pk')
        return query.filter(region=region)


########################################## RATING #######################################
@extend_schema(tags=['rating'])
class RatingCreateAPIView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [CustomerPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['rating'])
class RatingEmployerListAPIView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [CustomerPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Rating.objects.filter(user=user)
        return queryset


@extend_schema(tags=['rating'])
class RatingUpdateAPIView(UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingUpdateSerializer
    permission_classes = [CustomerPermission]


@extend_schema(tags=['rating'])
<<<<<<< HEAD
=======
class RatingDeleteAPIView(DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['rating'])
class RatingsListAPIView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['rating'])
>>>>>>> b3b3e91 (updated)
class RatingDetailAPIView(RetrieveAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    lookup_field = 'pk'


########################################## RATING IMAGES #######################################
@extend_schema(tags=['rating-images'])
class RatingImagesCreateAPIView(CreateAPIView):
    queryset = RatingImages.objects.all()
    serializer_class = RatingImagesModelSerializer
    permission_classes = [CustomerPermission]


@extend_schema(tags=['rating-images'])
class RatingImagesUpdateAPIView(UpdateAPIView):
    queryset = RatingImages.objects.all()
    serializer_class = RatingImagesModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['rating-images'])
class RatingImagesDeleteAPIView(DestroyAPIView):
    queryset = RatingImages.objects.all()
    serializer_class = RatingImagesModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['rating-images'])
class RatingImagesListAPIView(ListAPIView):
    queryset = RatingImages.objects.all()
    serializer_class = RatingImagesModelSerializer
    permission_classes = [CustomerPermission]


@extend_schema(tags=['rating-images'])
class RatingImagesRetrieveAPIView(RetrieveAPIView):
    queryset = RatingImages.objects.all()
    serializer_class = RatingImagesModelSerializer
    lookup_field = 'pk'
<<<<<<< HEAD
=======
>>>>>>> 88985c8 (updated)
>>>>>>> b3b3e91 (updated)
