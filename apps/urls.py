from django.urls import path

from apps.views import WorkCreateApi, LatestWorkListApi, EmployerWorksListApi, RegionListAPiView, WorkUpdateApi, \
    RatingEmployerListAPIView, RatingCreateAPIView, RatingUpdateAPIView, DistrictListAPiView, WorkerWorksListApi, \
<<<<<<< HEAD
    RatingImagesCreateAPIView, RatingImagesListAPIView, RatingImagesRetrieveAPIView, RatingDetailAPIView
=======
    RatingImagesCreateAPIView, RatingImagesListAPIView, RatingDeleteAPIView, RatingsListAPIView, \
    RatingImagesUpdateAPIView, RatingImagesDeleteAPIView, RatingImagesRetrieveAPIView, RatingDetailAPIView
>>>>>>> b3b3e91 (updated)

urlpatterns = [
    path('work-create', WorkCreateApi.as_view()),
    path('work-latest', LatestWorkListApi.as_view()),
    path('employer-works/<int:employer_id>', EmployerWorksListApi.as_view()),
    path('worker-works/<int:worker_id>', WorkerWorksListApi.as_view()),
    path('regions', RegionListAPiView.as_view()),
    path('districts/<int:region_pk>', DistrictListAPiView.as_view()),
    path('work-update/<int:pk>', WorkUpdateApi.as_view()),
]

urlpatterns += [
    path('rating-create', RatingCreateAPIView.as_view()),
    path('rating-update/<int:pk>', RatingUpdateAPIView.as_view()),
<<<<<<< HEAD
    path('rating-detail/<int:pk>', RatingDetailAPIView.as_view()),
    path('ratings-employer/<int:pk>', RatingEmployerListAPIView.as_view()),
=======
    path('rating-delete/<int:pk>', RatingDeleteAPIView.as_view()),
    path('rating-detail/<int:pk>', RatingDetailAPIView.as_view()),
    path('ratings-employer/<int:pk>', RatingEmployerListAPIView.as_view()),
    path('ratings', RatingsListAPIView.as_view()),
>>>>>>> b3b3e91 (updated)
]

urlpatterns += [
    path('rating-images-create', RatingImagesCreateAPIView.as_view()),
<<<<<<< HEAD
=======
    path('rating-images-update/<int:pk>', RatingImagesUpdateAPIView.as_view()),
    path('rating-images-delete/<int:pk>', RatingImagesDeleteAPIView.as_view()),
>>>>>>> b3b3e91 (updated)
    path('rating-images-detail/<int:pk>', RatingImagesRetrieveAPIView.as_view()),
    path('rating-images', RatingImagesListAPIView.as_view()),
]
