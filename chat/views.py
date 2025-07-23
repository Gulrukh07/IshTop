from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.models import Work
from chat.models import Chat
from chat.serializers import ChatModelSerializer


# Create your views here.
@extend_schema(tags=['chat'])
class ChatCreateApiView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        work_id = self.kwargs.get('work_pk')
        work = Work.objects.get(pk=work_id)
        receiver = self.kwargs.get('receiver_pk')
        serializer.save(sender=self.request.user,receiver_id= receiver,work=work )

@extend_schema(tags=['chat'])
class ChatListApiView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatModelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"sender_id": self.request.user.id})
        return context

    def get_queryset(self):
        query = super().get_queryset()
        sender = self.kwargs.get('sender_id')
        receiver = self.kwargs.get('receiver_id')
        queryset = query.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver,receiver=sender)).order_by('-created_at')
        return queryset


