from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authenticate.views import UserCreateAPIView, WorkerAdditionalCreateAPIView, UserRetrieveAPIView

urlpatterns = [
    path('create-user', UserCreateAPIView.as_view()),
    path('user-detail', UserRetrieveAPIView.as_view()),
    path('user-update', UserRetrieveAPIView.as_view()),
    path('create-additional-info', WorkerAdditionalCreateAPIView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
