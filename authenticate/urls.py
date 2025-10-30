from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authenticate.views import UserCreateAPIView, WorkerAdditionalCreateAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, ChangePasswordAPIView, WorkerAdditionalUpdateAPIView, SendOTPView, VerifyOTPView

app_name = 'auth'

urlpatterns = [
    path('register', UserCreateAPIView.as_view()),
    path('user-detail/<int:pk>', UserRetrieveAPIView.as_view()),
    path('user-update/<int:pk>', UserUpdateAPIView.as_view(), name='user-update'),
    path('create-additional-info', WorkerAdditionalCreateAPIView.as_view()),
    path('change-password/<int:pk>', ChangePasswordAPIView.as_view(), name='change-password'),
    path('worker-additional-update/<int:pk>', WorkerAdditionalUpdateAPIView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp")
]
