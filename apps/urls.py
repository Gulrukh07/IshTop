from django.urls import path

from apps.views import WorkCreateApi, LatestWorkListApi, EmployerWorksListApi, RegionListAPiView

urlpatterns = [
    path('work-create', WorkCreateApi.as_view()),
    path('work-latest', LatestWorkListApi.as_view()),
    path('employer-works/<int:employer_id>', EmployerWorksListApi.as_view()),
    path('regions', RegionListAPiView.as_view()),
]