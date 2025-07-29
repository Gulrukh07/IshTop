from ckeditor.fields import RichTextField
from django.db.models import Model, ForeignKey, SET_NULL, ImageField, CharField, DecimalField, TextField, IntegerField, \
    CASCADE, DateTimeField
from django.db.models.enums import TextChoices
from django.utils.translation import gettext as _


class Category(Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Region(Model):
    name = CharField(max_length=50)


class District(Model):
    name = CharField(max_length=50)
    region = ForeignKey('apps.Region', CASCADE, related_name='districts')


class Work(Model):
    class OrderStatus(TextChoices):
        NEW = 'new', _('New')
        COMPLETED = 'completed', _('Completed')
        CANCELED = 'canceled', _('Canceled')

    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', SET_NULL, null=True, blank=True, related_name='works')
    district = ForeignKey('apps.District', on_delete=SET_NULL, null=True, blank=True, related_name='works')
    latitude = DecimalField(decimal_places=10, max_digits=20)
    longitude = DecimalField(decimal_places=10, max_digits=20)
    price = DecimalField(decimal_places=0, max_digits=20)
    description = TextField()
    num_workers = IntegerField()
    employer = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='employer_works')
    worker = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='worker_works', null=True)
    status = CharField(max_length=120, choices=OrderStatus.choices, default=OrderStatus.NEW)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rating(Model):
    class StarsNumber(TextChoices):
        FIVE = '5', _('Five')
        FOUR = '4', _('Four')
        THREE = '3', _('Three')
        TWO = '2', _('Two')
        ONE = '1', _('One')

    stars = CharField(max_length=10, choices=StarsNumber.choices, default=StarsNumber.FIVE)
    comment = RichTextField()
    work = ForeignKey('apps.Work', on_delete=CASCADE, related_name='ratings')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    user = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='ratings')

    def __str__(self):
        return self.stars


class RatingImages(Model):
    image = ImageField(upload_to='rating_images', null=True, blank=True)
    rating = ForeignKey('apps.Rating', on_delete=CASCADE, related_name='images')


class Image(Model):
    work = ForeignKey('apps.Work', on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='work/images/%Y/%m/%d')


class Order(Model):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        DEAL = 'deal', 'Deal'
        CANCELED = 'canceled', 'Canceled'

    amount = DecimalField(decimal_places=0, max_digits=20)
    work = ForeignKey('apps.Work', on_delete=CASCADE, null=True, blank=True, related_name='orders')
    status = CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Payment(Model):
    class Status(TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    order = ForeignKey('apps.Order', on_delete=CASCADE, related_name='payments')
    amount = DecimalField(decimal_places=0, max_digits=20)
    status = CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Message(Model):
    text = TextField()
    user = ForeignKey('authenticate.User', on_delete=CASCADE, related_name='messages')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
