from datetime import datetime

import pytest
from rest_framework.test import APIClient

from apps.models import Work, Category, Region, District
from authenticate.models import User
from chat.models import Chat


# Create your tests here.

class TestChat:
    @pytest.fixture
    def api_client(self):
        user1 = User.objects.create(id=1,phone_number=+998997174716)
        user1.set_password("1")
        user1.save()

        user2 = User.objects.create(id=2,phone_number=+998997174717)
        user2.set_password("2")
        user2.save()

        category = Category.objects.create(id=1,
                                           name="test")
        region = Region.objects.create(id=1,name="test")
        district = District.objects.create(name="test",region_id=region.id)

        work = Work.objects.create(id=1,
                                   name="work1",
                            category=category,
                            latitude=1234567890,
                            longitude=1234567890,
                            description="work1",
                            employer=user2,
                            price=1000,
                            num_workers=3,
                            status=Work.OrderStatus.NEW,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            district=district,
                            )
        Chat.objects.create(sender=user1, receiver=user2, work=work, content='hello world',
                            created_at=datetime.now(),updated_at=datetime.now())

        return APIClient()

    @pytest.mark.django_db
    def test_chat_list(self, api_client):
        login_url = 'http://127.0.0.1:8000/api/v1/login'
        response = api_client.post(login_url , data={"phone_number": +998997174716 , "password":1})
        assert response.status_code == 200
        assert "access" in response.json().keys()
        access_token = response.json().get('access')
        url = 'http://0.0.0.0:8000/api/v1/chat-list/2/1'
        response = api_client.get(url, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 200

