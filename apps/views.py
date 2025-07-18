from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Work
from apps.permissions import CustomerPermission
from apps.serializers import WorkModelSerializer


# Create your views here.
@extend_schema(tags=['Work'])
class WorkCreateApi(CreateAPIView):
    queryset = Work
    serializer_class = WorkModelSerializer
    permission_classes = [IsAuthenticated,CustomerPermission]

    def perform_create(self, serializer):

        serializer.save(employer = self.request.user)




@extend_schema(tags=['Work'])
class LatestWorkListApi(ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkModelSerializer

    def get_queryset(self):
        query = super().get_queryset().filter(worker = None).order_by('-created_at')
        return query

@extend_schema(tags=['Work'])
class EmployerWorksListApi(ListAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkModelSerializer

    def get_queryset(self):
        employer_id = self.kwargs.get('employer_id')
        return super().get_queryset().filter(employer=employer_id)


