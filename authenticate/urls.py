from django.urls import path

from authenticate.views import UserCreateAPIView

urlpatterns = [
    path('create-user', UserCreateAPIView.as_view()),

]
