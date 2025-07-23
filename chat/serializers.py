from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from authenticate.models import User
from chat.models import Chat


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name',

class ChatModelSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields =  'content', 'receiver'
        read_only_fields = ('id', 'created_at', 'updated_at','sender', 'receiver', 'work')

    def validate_receiver(self, value):
        sender_id = self.context.get('sender_id', None)
        if value == sender_id:
            raise ValidationError("Siz o'zingizga xabar yuboraolmaysiz")
        return value