from django.urls import path

from chat.views import ChatListApiView, ChatCreateApiView

urlpatterns = [
    path('chat-list/<int:sender_id>/<int:receiver_id>', ChatListApiView.as_view()),
    path('chat-create/<int:work_pk>/<int:receiver_pk>', ChatCreateApiView.as_view()),
]