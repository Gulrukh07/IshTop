from django.urls import path

from apps.views import WorkCreateApi, LatestWorkListApi, EmployerWorksListApi, RegionListAPiView, WorkUpdateApi, \
    DistrictListAPiView

urlpatterns = [
    path('work-create', WorkCreateApi.as_view()),
    path('work-latest', LatestWorkListApi.as_view()),
    path('employer-works/<int:employer_id>', EmployerWorksListApi.as_view()),
    path('regions', RegionListAPiView.as_view()),
    path('districts/<int:region_pk>', DistrictListAPiView.as_view()),
    path('work-update/<int:pk>', WorkUpdateApi.as_view()),
]