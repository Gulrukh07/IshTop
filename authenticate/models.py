from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import CharField, DecimalField, DateTimeField, ImageField, Model, ForeignKey, SET_NULL, \
    OneToOneField
from django.db.models.enums import TextChoices

from apps.models import Region, District


class CustomUserManager(UserManager):
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

    create_superuser.alters_data = True

    async def acreate_superuser(
            self, phone_number, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return await self._acreate_user(phone_number, password, **extra_fields)

    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class RoleType(TextChoices):
        EMPLOYER = 'employer', 'Employer'
        ADMIN = 'admin', 'Admin'
        WORKER = 'worker', 'Worker'

    phone_number = CharField(max_length=15, unique=True)
    role = CharField(max_length=50, choices=RoleType.choices)
    balance = DecimalField(decimal_places=0, max_digits=20, default=0)
    avatar = ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    registered_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    username = None
    email = None
    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class WorkerAdditional(Model):
    class Meta:
        unique_together = ("passport_seria", "passport_number")

    class Gender(TextChoices):
        MALE = 'male', "Male"
        FEMALE = "female", "Female"

    user = OneToOneField(User, on_delete=SET_NULL, null=True, related_name="workeradditional")
    gender = CharField(max_length=10, choices=Gender.choices)
    passport_seria = CharField(max_length=2)
    passport_number = CharField(max_length=7)
    district = ForeignKey('apps.District', SET_NULL, null=True, blank=True, related_name='workers')
