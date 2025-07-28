from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Work, Region, District
from apps.permissions import CustomerPermission
from apps.serializers import WorkModelSerializer, DistrictSerializer, WorkSerializer, \
    RegionModelSerializer


# Create your views here.
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
