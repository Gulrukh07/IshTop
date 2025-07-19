from datetime import datetime

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from authenticate.models import User, WorkerAdditional, Region


class TestAuth:
    @pytest.fixture
    def api_client(self):
        region = Region.objects.create(
            pk=1,
            name='Tashkent'
        )
        user = User.objects.create_user(
            pk=1,
            full_name='Ali',
            phone_number='+998971234567',
            password='@Ag562',
            role=User.RoleType.EMPLOYER,
            date_joined=datetime.now(),
            balance=500000,
            registered_at=datetime.now(),
            updated_at=datetime.now(),
        )

        work_addtional = WorkerAdditional.objects.create(
            pk=1,
            gender='male',
            user=user,
            passport_seria='AA',
            passport_number='1234567',
            region=region,
        )

        return APIClient()

    def test_create_user(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+9989012",
            "password": "@smth2",
            "avatar": None,
            "role": "employer"
        })
        assert response.status_code == 201
        assert response.data['first_name'] == 'Ali'

    def test_invalid_phone_number(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+9989712",
            "password": "@smth2",
            "avatar": None,
            "role": "employer"
        })
        assert response.status_code == 400
        assert 'Phone number' in str(response.data)

    def test_invalid_password(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+998971234567",
            "password": "@smth2",
            "avatar": None,
            "role": "employer"
        })
        assert response.status_code == 400
        assert 'Password must be at least' in str(response.data)

    def test_invalid_avatar(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        file = SimpleUploadedFile('avatar.txt', b'file_content', content_type='text/plain')
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+998971234567",
            "password": "@smth2",
            "avatar": file,
            "role": "employer"
        })
        assert response.status_code == 400
        assert 'Avatar must be an image' in str(response.data)
