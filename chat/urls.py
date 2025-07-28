from django.urls import path

from chat.views import ChatListApiView

urlpatterns = [
    path('chat-list/<int:sender_id>/<int:receiver_id>', ChatListApiView.as_view()),
]
