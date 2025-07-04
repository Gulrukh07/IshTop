from django.urls import path

from authenticate.views import UserCreateAPIView, WorkerAdditionalCreateAPIView

urlpatterns = [
    path('create-user', UserCreateAPIView.as_view()),
    path('create-additional-info', WorkerAdditionalCreateAPIView.as_view()),

]
