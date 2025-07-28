from datetime import datetime

import pytest
from rest_framework.test import APIClient

from apps.models import Work, Category, District
from authenticate.models import User, Region


class TestWork:
    @pytest.fixture
    def api_client(self):
        user = User.objects.create(phone_number=+998997174716)
        user.set_password("1")
        user.save()

        category = Category.objects.create(id=1,
                                           name="test")
        region = Region.objects.create(id=1, name="test")
        district = District.objects.create(name="test", region_id=region.id)

        Work.objects.create(name="work1",
                            category=category,
                            latitude=1234567890,
                            longitude=1234567890,
                            description="work1",
                            employer=user,
                            price=1000,
                            num_workers=3,
                            status=Work.OrderStatus.NEW,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            district=district,
                            )
        Work.objects.create(name="work2",
                            category=category,
                            latitude=1234567890,
                            longitude=1234567890,
                            description="work2",
                            employer=user,
                            price=1000,
                            num_workers=3,
                            status=Work.OrderStatus.NEW,
                            created_at=datetime.now(),
                            updated_at=datetime.now(),
                            district=district,
                            )

        return APIClient()

    @pytest.mark.django_db
    def test_work_create(self, api_client: APIClient):
        login_url = 'http://127.0.0.1:8000/api/v1/login'
        response = api_client.post(login_url, data={"phone_number": +998997174716, "password": 1})
        assert response.status_code == 200
        assert "access" in response.json().keys()
        access_token = response.json().get('access')
        url = 'http://127.0.0.1:8000/api/v1/work-create'
        user = User.objects.get(pk=1)
        category = Category.objects.get(pk=1)
        district = District.objects.get(pk=1)
        response1 = api_client.post(url, headers={"Authorization": f"Bearer {access_token}"},
                                    data={'category': category.pk,
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
                                          'district': district.pk,
                                          })
        response2 = api_client.post(url, headers={"Authorization": f"Bearer {access_token}"},
                                    data={'category': 1000,
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
                                          'region': district.pk,
                                          })
        response3 = api_client.post(url, headers={"Authorization": f"Bearer {access_token}"},
                                    data={'category': category.pk,
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
                                          'region': district.pk,
                                          })
        response4 = api_client.post(url, headers={"Authorization": f"Bearer {access_token}"},
                                    data={'category': category.pk,
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
                                          'district': district.pk,
                                          })
        response5 = api_client.post(url, headers={"Authorization": f"Bearer {access_token}"},
                                    data={'category': category.pk,
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
                                          'district': 5,
                                          })

        assert response1.status_code == 201
        assert response2.status_code == 400
        assert response2.json().get('category') == [
            "Invalid pk \"1000\" - object does not exist."
        ]
        assert response3.status_code
        assert response3.json().get("price") == [
            "Narx faqat raqamalardan iborat musbat son bo'lsin"
        ]
        assert response4.status_code == 400
        assert response4.json().get('num_workers') == [
            "Ishchilar soni faqat raqamalardan iborat musbat son bo'lsin"
        ]
        assert response5.status_code == 400
        assert response5.json().get('district') == [
            "Invalid pk \"5\" - object does not exist."
        ]

    @pytest.mark.django_db
    def test_work_latest(self, api_client: APIClient):
        url = "http://127.0.0.1:8000/api/v1/work-latest"
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    @pytest.mark.django_db
    def test_employer_work(self, api_client: APIClient):
        url = 'http://127.0.0.1:8000/api/v1/employer-works/1'
        response = api_client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_work_put(self, api_client: APIClient):
        user = User.objects.get(id=1)
        category = Category.objects.get(id=1)
        district = District.objects.get(id=1)
        login_url = 'http://0.0.0.0:8000/api/v1/login'
        response = api_client.post(login_url, data={"phone_number": +998997174716, "password": 1})
        assert response.status_code == 200
        assert "access" in response.json().keys()
        access_token = response.json().get('access')
        url = 'http://0.0.0.0:8000/api/v1/work-update/1'
        response1 = api_client.put(url, headers={"Authorization": f"Bearer {access_token}"})
        response2 = api_client.put(url, data={"name": "work10",
                                              "category": category.pk,
                                              "latitude": 1234567890,
                                              "longitude": 1234567890,
                                              "description": "work1",
                                              "employer": user.pk,
                                              "price": 1000,
                                              "num_workers": 3,
                                              "status": Work.OrderStatus.NEW,
                                              "created_at": datetime.now(),
                                              "updated_at": datetime.now(),
                                              "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )
        response3 = api_client.put(url, data={
            "category": category.pk,
            "latitude": 1234567890,
            "longitude": 1234567890,
            "description": "work1",
            "employer": user.pk,
            "price": 1000,
            "num_workers": 3,
            "status": Work.OrderStatus.NEW,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )
        response4 = api_client.put(url, data={"name": "work10",
                                              "latitude": 1234567890,
                                              "longitude": 1234567890,
                                              "description": "work1",
                                              "employer": user.pk,
                                              "price": 1000,
                                              "num_workers": 3,
                                              "status": Work.OrderStatus.NEW,
                                              "created_at": datetime.now(),
                                              "updated_at": datetime.now(),
                                              "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )

        response5 = api_client.put(url, data={"name": "work10",
                                              "category": category.pk,
                                              "longitude": 1234567890,
                                              "description": "work1",
                                              "employer": user.pk,
                                              "price": 1000,
                                              "num_workers": 3,
                                              "status": Work.OrderStatus.NEW,
                                              "created_at": datetime.now(),
                                              "updated_at": datetime.now(),
                                              "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )
        response6 = api_client.put(url, data={"name": "work10",
                                              "category": category.pk,
                                              "latitude": 1234567890,
                                              "description": "work1",
                                              "employer": user.pk,
                                              "price": 1000,
                                              "num_workers": 3,
                                              "status": Work.OrderStatus.NEW,
                                              "created_at": datetime.now(),
                                              "updated_at": datetime.now(),
                                              "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )
        response7 = api_client.put(url, data={"name": "work10",
                                              "category": category.pk,
                                              "latitude": 1234567890,
                                              "longitude": 1234567890,
                                              "employer": user.pk,
                                              "price": 1000,
                                              "num_workers": 3,
                                              "status": Work.OrderStatus.NEW,
                                              "created_at": datetime.now(),
                                              "updated_at": datetime.now(),
                                              "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )
        response9 = api_client.put(url, data={"name": "work10",
                                              "category": category.pk,
                                              "latitude": 1234567890,
                                              "longitude": 1234567890,
                                              "description": "work1",
                                              "employer": user.pk,
                                              "num_workers": 3,
                                              "status": Work.OrderStatus.NEW,
                                              "created_at": datetime.now(),
                                              "updated_at": datetime.now(),
                                              "district": district.pk, },
                                   headers={"Authorization": f"Bearer {access_token}"}
                                   )
        response10 = api_client.put(url, data={"name": "work10",
                                               "category": category.pk,
                                               "latitude": 1234567890,
                                               "longitude": 1234567890,
                                               "description": "work1",
                                               "employer": user.pk,
                                               "price": 1000,
                                               "status": Work.OrderStatus.NEW,
                                               "created_at": datetime.now(),
                                               "updated_at": datetime.now(),
                                               "district": district.pk, },
                                    headers={"Authorization": f"Bearer {access_token}"}
                                    )
        response11 = api_client.put(url, data={"name": "work10",
                                               "category": category.pk,
                                               "latitude": 1234567890,
                                               "longitude": 1234567890,
                                               "description": "work1",
                                               "employer": user.pk,
                                               "price": 1000,
                                               "num_workers": 3,
                                               "status": Work.OrderStatus.NEW,
                                               "created_at": datetime.now(),
                                               "updated_at": datetime.now(),
                                               },
                                    headers={"Authorization": f"Bearer {access_token}"}
                                    )
        assert response1.status_code == 400
        assert response2.status_code == 200
        assert response3.status_code == 400
        assert response3.json().get('name') == ['This field is required.']
        assert response4.status_code == 400
        assert response4.json().get('category') == ['This field is required.']
        assert response5.status_code == 400
        assert response5.json().get('latitude') == ['This field is required.']
        assert response6.status_code == 400
        assert response6.json().get('longitude') == ['This field is required.']
        assert response7.status_code == 400
        assert response7.json().get('description') == ['This field is required.']
        assert response9.status_code == 400
        assert response9.json().get('price') == ['This field is required.']
        assert response10.status_code == 400
        assert response10.json().get('num_workers') == ['This field is required.']

        assert response11.status_code == 400
        assert response11.json().get('district') == ['This field is required.']

    @pytest.mark.django_db
    def test_work_patch(self, api_client: APIClient):
        login_url = 'http://0.0.0.0:8000/api/v1/login'
        response = api_client.post(login_url, data={"phone_number": "998997174716", "password": "1"})
        assert response.status_code == 200
        access_token = response.json().get('access')
        assert access_token is not None

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        new_category = Category.objects.create(name="New Category")
        district = District.objects.get(pk=1)
        work = Work.objects.get(pk=1)

        url = 'http://127.0.0.1:8000/api/v1/work-update/1'

        response1 = api_client.patch(url, format='json')
        assert response1.status_code == 200
        assert response1.json().get("name") == work.name
        if work.district:
            assert response1.json().get("district")["id"] == district.pk

        response2 = api_client.patch(url, data={"name": "Updated work", "district": district.pk},
                                     format='json')
        assert response2.status_code == 200
        assert response2.json().get("name") == "Updated work"
        assert response2.json().get("district")["id"] == district.pk

        response3 = api_client.patch(url, data={"name": "Another name"}, format='json')
        assert response3.status_code == 200
        assert response3.json().get("name") == "Another name"

        response4 = api_client.patch(url, data={"district": district.pk}, format='json')
        assert response4.status_code == 200
        assert response4.json().get("district")["id"] == district.pk

        response6 = api_client.patch(url, data={"num_workers": 5}, format='json')
        assert response6.status_code == 200
        assert response6.json().get("num_workers") == 5

        response7 = api_client.patch(url, data={"category": new_category.pk}, format='json')
        assert response7.status_code == 200
        assert response7.json().get("category")["id"] == new_category.pk
