from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authenticate.views import UserCreateAPIView, WorkerAdditionalCreateAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, ChangePasswordAPIView, WorkerAdditionalUpdateAPIView, UserListAPIView, UserDeleteAPIView

app_name = 'auth'

urlpatterns = [
    path('create-user', UserCreateAPIView.as_view()),
    path('user-detail/<int:pk>', UserRetrieveAPIView.as_view()),
    path('user-update/<int:pk>', UserUpdateAPIView.as_view()),
    path('user-delete/<int:pk>', UserDeleteAPIView.as_view()),
    path('users', UserListAPIView.as_view()),
    path('create-additional-info', WorkerAdditionalCreateAPIView.as_view()),
    path('change-password/<int:pk>', ChangePasswordAPIView.as_view(), name='change-password'),
    path('worker-additional-update/<int:pk>', WorkerAdditionalUpdateAPIView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
