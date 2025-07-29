from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Work, Region, District, Rating
from apps.permissions import CustomerPermission
from apps.serializers import WorkModelSerializer, DistrictSerializer, WorkSerializer, \
    RegionModelSerializer, RatingModelSerializer


@extend_schema(tags=['Work'])
class WorkCreateApi(CreateAPIView):
    queryset = Work
    serializer_class = WorkModelSerializer
    permission_classes = [IsAuthenticated, CustomerPermission]

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
    permission_classes = [IsAuthenticated, CustomerPermission]
    queryset = Work
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


@extend_schema(tags=['rating'], request=RatingModelSerializer, responses=RatingModelSerializer)
class RatingCreateAPIView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [IsAuthenticated, CustomerPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['rating'], request=RatingModelSerializer, responses=RatingModelSerializer)
class RatingEmployerListAPIView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer
    permission_classes = [IsAuthenticated, CustomerPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Rating.objects.filter(user=user)
        return queryset


@extend_schema(tags=['rating'], request=RatingModelSerializer, responses=RatingModelSerializer)
class RatingUpdateAPIView(UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingModelSerializer

# @extend_schema(tags=['Payment'])
# class PaymentCreateApi(CreateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class =
#     permission_classes = [IsAuthenticated, CustomerPermission]
