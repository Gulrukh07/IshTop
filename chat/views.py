from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from chat.models import Chat
from chat.serializers import ChatModelSerializer


# Create your views here.

@extend_schema(tags=['chat'])
class ChatListApiView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatModelSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        query = super().get_queryset()
        sender = self.kwargs.get('sender_id')
        receiver = self.kwargs.get('receiver_id')
        queryset = query.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver,receiver=sender)).order_by('-created_at')
        return queryset


