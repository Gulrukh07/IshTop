from django.db.models import Model, ForeignKey, CASCADE, TextField, DateTimeField

from apps.models import Work
from authenticate.models import User


# Create your models here.

class Chat(Model):
    work = ForeignKey('apps.Work', on_delete=CASCADE)
    sender = ForeignKey(User, related_name='sender', on_delete=CASCADE)
    receiver = ForeignKey(User, related_name='receiver', on_delete=CASCADE)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
