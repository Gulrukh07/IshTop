from datetime import datetime

import pytest

from apps.models import Work, Category
from rest_framework.test import APIClient

from authenticate.models import User, Region


class TestWork:
    @pytest.fixture
    def api_client(self):
        user = User.objects.create(username="admin")
        user.set_password("1")
        user.save()

        category = Category.objects.create(name="test")
        region = Region.objects.create(name="test")

        Work.objects.create(name="work1",
                            category=category.pk,
                            latitude=1234567890,
                            longitude=1234567890,
                            description="work1",
                            employer=user.pk,
                            price=1000,
                            num_workers=3,
                            status=Work.OrderStatus.NEW,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            region=region.pk,
                            )
        Work.objects.create(name="work2",
                            category=category.pk,
                            latitude=1234567890,
                            longitude=1234567890,
                            description="work2",
                            employer=user.pk,
                            price=1000,
                            num_workers=3,
                            status=Work.OrderStatus.NEW,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            region=region.pk,
                            )

        return APIClient()

    @pytest.mark.django_db
    def test_work_create(self, api_client:APIClient):
        url = 'http://127.0.0.1:8000/api/v1/work-create'
        user = User.objects.get(pk=1)
        category = Category.objects.get(pk=1)
        region = Region.objects.get(pk=1)
        response1 = api_client.post(url, data={'category': category.pk,
                                               'name': 'Work 1',
                                               'description': 'work description',
                                               'price': 1000,
                                               'num_workers': 3,
                                               'status': Work.OrderStatus.NEW,
                                               'created_at': datetime.now(),
                                               'updated_at': datetime.now(),
                                               'employer': user.pk,
                                               'latitude': 1234567890,
                                               'longitude': 1234567890,
                                               'region': region.pk,
                                               })
        response2 = api_client.post(url, data={'category': 2,
                                               'name': 'Work 1',
                                               'description': 'work description',
                                               'price': 1000,
                                               'num_workers': 3,
                                               'status': Work.OrderStatus.NEW,
                                               'created_at': datetime.now(),
                                               'updated_at': datetime.now(),
                                               'employer': user.pk,
                                               'latitude': 1234567890,
                                               'longitude': 1234567890,
                                               'region': region.pk,
                                               })
        response3 = api_client.post(url, data={'category': category.pk,
                                               'name': 'Work 1',
                                               'description': 'work description',
                                               'price': -1000,
                                               'num_workers': 3,
                                               'status': Work.OrderStatus.NEW,
                                               'created_at': datetime.now(),
                                               'updated_at': datetime.now(),
                                               'employer': user.pk,
                                               'latitude': 1234567890,
                                               'longitude': 1234567890,
                                               'region': region.pk,
                                               })
        response4 = api_client.post(url, data={'category': category.pk,
                                               'name': 'Work 1',
                                               'description': 'work description',
                                               'price': 1000,
                                               'num_workers': -3,
                                               'status': Work.OrderStatus.NEW,
                                               'created_at': datetime.now(),
                                               'updated_at': datetime.now(),
                                               'employer': user.pk,
                                               'latitude': 1234567890,
                                               'longitude': 1234567890,
                                               'region': region.pk,
                                               })
        response5 = api_client.post(url, data={'category': category.pk,
                                               'name': 'Work 1',
                                               'description': 'work description',
                                               'price': 1000,
                                               'num_workers': 3,
                                               'status': Work.OrderStatus.NEW,
                                               'created_at': datetime.now(),
                                               'updated_at': datetime.now(),
                                               'employer': user.pk,
                                               'latitude': 1234567890,
                                               'longitude': 1234567890,
                                               'region': 5,
                                               })


        assert response1.status_code == 201
        assert response2.status_code ==400
        assert response2.json().get('category') == [
            "Invalid pk \"3\" - object does not exist."
        ]
        assert response3.status_code == 400
        assert response3.json().get('price') == [
            "Narx faqat raqamalardan iborat musbat son bo'lsin"
        ]
        assert response4.status_code == 400
        assert response4.json().get('num_workers') == [
            "Ishchilar soni faqat raqamalardan iborat musbat son bo'lsin"
        ]
        assert response5.status_code == 400
        assert response5.json().get('region') == [
            "Invalid pk \"4\" - object does not exist."
        ]



