from django.urls import path

from apps.views import WorkCreateApi, LatestWorkListApi, EmployerWorksListApi, RegionListAPiView, WorkUpdateApi, \
    RatingEmployerListAPIView, RatingCreateAPIView, RatingUpdateAPIView, DistrictListAPiView, WorkerWorksListApi, \
    RatingImagesCreateAPIView, RatingImagesListAPIView

urlpatterns = [
    path('work-create', WorkCreateApi.as_view()),
    path('work-latest', LatestWorkListApi.as_view()),
    path('employer-works/<int:employer_id>', EmployerWorksListApi.as_view()),
    path('worker-works/<int:worker_id>', WorkerWorksListApi.as_view()),
    path('regions', RegionListAPiView.as_view()),
    path('districts/<int:region_pk>', DistrictListAPiView.as_view()),
    path('work-update/<int:pk>', WorkUpdateApi.as_view()),
    path('rating-create', RatingCreateAPIView.as_view()),
    path('rating-update/<int:pk>', RatingUpdateAPIView.as_view()),
    path('ratings-employer/<int:pk>', RatingEmployerListAPIView.as_view()),
    path('rating-images-create', RatingImagesCreateAPIView.as_view()),
    path('rating-images', RatingImagesListAPIView.as_view()),
]
