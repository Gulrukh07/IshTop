import io

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.models import District, Region
from authenticate.models import User, WorkerAdditional
from authenticate.serializers import UserUpdateSerializer, WorkerAdditionalSerializer, WorkerAdditionalUpdateSerializer


class TestAuth:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    def setup_method(self):
        image_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), color="green")
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        avatar = SimpleUploadedFile("avatar.jpg", image_io.read(), content_type="image/jpeg")

        self.user = User.objects.create_user(
            phone_number="+998971234566",
            password="Test123",
            first_name="John",
            last_name="Doe",
            role='worker',
            avatar=avatar,
        )
        self.serializer_data = {
            "first_name": "Go'zal",
            "last_name": "Abdujabborova",
            "avatar": None
        }

    @pytest.mark.django_db
    def test_create_user(self, api_client):
        url = '/api/v1/create-user'
        response = api_client.post(url, data={
            "first_name": "Ali",
            "last_name": "Aliyev",
            "phone_number": "+998901234567",
            "password": "@smth2",
            "role": "employer"
        }, format='json')

        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.data}"
        assert response.data['first_name'] == 'Ali'

    @pytest.mark.django_db
    def test_invalid_phone_number(self, api_client):
        url = '/api/v1/create-user'
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
        url = '/api/v1/create-user'
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
        url = '/api/v1/create-user'
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
    def test_update_valid_data(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('auth:user-update', kwargs={'pk': self.user.pk})
        response = api_client.put(url, data=self.serializer_data, format='json')

        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.data}"
        self.user.refresh_from_db()
        assert self.user.first_name == "Go'zal"
        assert self.user.last_name == "Abdujabborova"
        assert not self.user.avatar
        assert self.user.phone_number == "+998971234566"

    @pytest.mark.django_db
    def test_partial_update(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('auth:user-update', kwargs={'pk': self.user.pk})
        partial_data = {'first_name': 'Asal'}
        response = api_client.patch(url, data=partial_data, format='json')

        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}: {response.data}"
        self.user.refresh_from_db()
        assert self.user.first_name == "Asal"
        assert self.user.last_name == "Doe"
        assert self.user.phone_number == '+998971234566'

    @pytest.mark.django_db
    def test_update_with_valid_avatar(self, api_client):
        image_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        avatar = SimpleUploadedFile("avatar.jpg", image_io.read(), content_type="image/jpeg")
        data = self.serializer_data.copy()
        data["avatar"] = avatar

        serializer = UserUpdateSerializer(instance=self.user, data=data)
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()

        assert updated_user.first_name == "Go'zal"
        assert updated_user.last_name == "Abdujabborova"
        assert updated_user.avatar.name.endswith(".jpg")

    @pytest.mark.django_db
    def test_update_with_invalid_avatar(self):
        invalid_avatar = SimpleUploadedFile("avatar.txt", b"file_content", content_type="text/plain")
        data = self.serializer_data.copy()
        data["avatar"] = invalid_avatar

        serializer = UserUpdateSerializer(instance=self.user, data=data)
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        assert "upload a valid image" in str(exc_info.value).lower()

    @pytest.mark.django_db
    def test_update_empty_data(self):
        serializer = UserUpdateSerializer(instance=self.user, data={}, partial=True)
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()

        assert updated_user.first_name == "John"
        assert updated_user.last_name == "Doe"
        assert updated_user.avatar

    @pytest.mark.django_db
    def test_update_read_only_fields(self):
        data = self.serializer_data.copy()
        data["phone_number"] = "998991234567"
        data["password"] = "NewPass123"

        serializer = UserUpdateSerializer(instance=self.user, data=data)
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()

        assert updated_user.first_name == "Go'zal"
        assert updated_user.last_name == "Abdujabborova"
        assert updated_user.phone_number == "+998971234566"
        assert updated_user.check_password("Test123")

    @pytest.mark.django_db
    def test_change_password_success(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('auth:change-password', kwargs={'pk': self.user.pk})

        data = {
            "old_password": "user_old_password",
            "new_password": "Newpass123",
            "confirm_password": "Newpass123"
        }

        self.user.set_password("user_old_password")
        self.user.save()

        response = api_client.put(url, data=data, format='json')
        assert response.status_code == 200

        self.user.refresh_from_db()
        assert self.user.check_password("Newpass123")

    @pytest.mark.django_db
    def test_change_password_wrong_old(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('auth:change-password', kwargs={'pk': self.user.pk})

        self.user.set_password("correct_old")
        self.user.save()

        data = {
            "old_password": "wrong_old",
            "new_password": "Newpass123",
            "confirm_password": "Newpass123"
        }

        response = api_client.put(url, data=data, format='json')
        assert response.status_code == 400
        assert "old_password" in response.data or "non_field_errors" in response.data

    @pytest.mark.django_db
    def test_change_password_mismatch_confirm(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('auth:change-password', kwargs={'pk': self.user.pk})

        self.user.set_password("correct_old")
        self.user.save()

        data = {
            "old_password": "correct_old",
            "new_password": "Newpass123",
            "confirm_password": "WrongConfirm"
        }

        response = api_client.put(url, data=data, format='json')
        assert response.status_code == 400
        assert "non_field_errors" in response.data

    @pytest.mark.django_db
    def test_retrieve_user(self, api_client):
        user = User.objects.create_user(
            first_name="Ali",
            last_name="Valiyev",
            phone_number="+998901234567",
            password="Pa$$word1!",
            role=User.RoleType.EMPLOYER
        )
        api_client.force_authenticate(user=user)
        url = f'/api/v1/user-detail/{user.id}'
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['first_name'] == "Ali"

    @pytest.mark.django_db
    def test_worker_additional_create(self, api_client):
        url = '/api/v1/create-additional-info'
        user = User.objects.create_user(
            phone_number="+998971234561",
            password="Test123",
            first_name="John",
            last_name="Doe",
            role='worker',
        )
        region = Region.objects.create(name="Toshkent")
        district = District.objects.create(name="Yunusobod", region=region)
        data = {
            "gender": "male",
            "passport_seria": "AA",
            "passport_number": "1234567",
            "district": district.id,
            "user": user.id
        }

        response = api_client.post(url, data)
        assert response.status_code == 201
        assert response.data['passport_number'] == "1234567"

    @pytest.mark.django_db
    def test_worker_additional_valid_data(self):
        user = User.objects.create_user(
            first_name="Ali",
            last_name="Valiyev",
            phone_number="+998901234567",
            password="Pa$$word1!",
            role=User.RoleType.WORKER
        )
        region = Region.objects.create(name="Toshkent")
        district = District.objects.create(name="Chilonzor", region=region)

        valid_data = {
            "gender": "male",
            "passport_seria": "AA",
            "passport_number": "1234567",
            "district": district.id,
            "user": user.id
        }
        serializer = WorkerAdditionalSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors

    @pytest.mark.django_db
    def test_invalid_passport_seria(self):
        data = {
            "gender": "male",
            "passport_seria": "ZZ",
            "passport_number": "1234567",
            "district": 1,
            "user": 1
        }
        serializer = WorkerAdditionalSerializer(data=data)
        assert not serializer.is_valid()
        assert "passport_seria" in serializer.errors

    @pytest.mark.django_db
    def test_invalid_passport_number(self):
        data = {
            "gender": "male",
            "passport_seria": "AA",
            "passport_number": "123",
            "district": 1,
            "user": 1
        }
        serializer = WorkerAdditionalSerializer(data=data)
        assert not serializer.is_valid()
        assert "passport_number" in serializer.errors

    @pytest.mark.django_db
    def test_update_work_additional(self, api_client):
        user = User.objects.create_user(
            first_name="Ali",
            last_name="Valiyev",
            phone_number="+998901234567",
            password="Pa$$word1!",
            role=User.RoleType.WORKER
        )
        region = Region.objects.create(name="Toshkent")
        district1 = District.objects.create(name="Yakkasaroy", region=region)
        district2 = District.objects.create(name="Chilonzor", region=region)

        worker_additional = WorkerAdditional.objects.create(
            user=user,
            gender='male',
            passport_seria='AA',
            passport_number='1234567',
            district=district1
        )

        data = {
            'district': district2.id
        }
        serializer = WorkerAdditionalUpdateSerializer(
            instance=worker_additional,
            data=data,
            partial=True
        )

        assert serializer.is_valid(), serializer.errors
        updated_instance = serializer.save()

        assert updated_instance.district == district2
