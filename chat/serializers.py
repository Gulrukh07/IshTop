from rest_framework.serializers import ModelSerializer

from authenticate.models import User
from chat.models import Chat


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name',

class MessageModelSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = 'sender', 'content', 'created_at'