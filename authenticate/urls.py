from django.urls import path

from authenticate.views import UserCreateAPIView, WorkerAdditionalCreateAPIView, UserRetrieveAPIView

urlpatterns = [
    path('create-user', UserCreateAPIView.as_view()),
    path('user-detail', UserRetrieveAPIView.as_view()),
    path('user-update', UserRetrieveAPIView.as_view()),
    path('create-additional-info', WorkerAdditionalCreateAPIView.as_view()),

]
