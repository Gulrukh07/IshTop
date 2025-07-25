import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from authenticate.models import User


class TestAuth:
    @pytest.fixture
    def api_client(self):
        # region = Region.objects.create(
        #     pk = 1,
        #     name='Tashkent'
        # )
        # user = User.objects.create_user(
        #     pk = 5,
        #     full_name='Ali',
        #     phone_number='+998971234567',
        #     password='@Ag562',
        #     role=User.RoleType.EMPLOYER,
        #     date_joined=datetime.now(),
        #     balance=500000,
        #     registered_at=datetime.now(),
        #     updated_at=datetime.now(),
        # )
        #
        # work_addtional = WorkerAdditional.objects.create(
        #     pk = 1,
        #     gender='male',
        #     user=user.pk,
        #     passport_seria='AA',
        #     passport_number='1234547',
        #     region=region,
        # )

        return APIClient()

    @pytest.mark.django_db
    def test_create_user(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+998901234567",
            "password": "@smth2",
            "role": "employer"
        }, format='multipart')

        assert response.status_code == 201
        assert response.data['first_name'] == 'Ali'

    @pytest.mark.django_db
    def test_invalid_phone_number(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+9989712",
            "password": "@smth2",
            "role": "employer"
        }, format='multipart')
        assert response.status_code == 400
        assert 'phone_number' in response.data
        assert "Telefon raqami quyidagi formatda bo‘lishi kerak: +998XXXXXXXXX" in str(response.data['phone_number'][0])

    @pytest.mark.django_db
    def test_invalid_password(self, api_client):
        url = 'http://localhost:8000/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+998971234567",
            "password": "123",
            "role": "employer"
        }, format='multipart')
        assert response.status_code == 400
        assert 'password' in response.data
        assert 'password must be at least' in str(response.data['password']).lower()

    @pytest.mark.django_db
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
        }, format='multipart')
        assert response.status_code == 400
        assert 'avatar' in response.data
        assert 'upload a valid image' in str(response.data['avatar']).lower()

    @pytest.mark.django_db
    def test_update_user(self, api_client):
        user = User.objects.create_user(
            first_name="Ali",
            last_name="Aliyev",
            phone_number="+998971234567",
            password="@smth2",
            role="employer"
        )
