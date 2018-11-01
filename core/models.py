from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class TimestampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PlannedTimestampModel(models.Model):
    planned_date = models.DateTimeField()


class CoreUser(AbstractUser):
    pass

class Rental(TimestampModel):
    name = models.CharField(
        max_length=255,
    )
    address = models.CharField(
        max_length=255,
    )
    rooms = models.IntegerField(default=1)
    price = models.IntegerField()
    image = models.ImageField()
    is_free = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return 'id=%d name=%s' % (self.id, self.name)


class Event(TimestampModel):
    VIEW = 0
    CHECK_IN = 1
    PAYMENT = 2
    CHECK_OUT = 3

    EVENT_CHOICES = (
        (VIEW, 'View'),
        (CHECK_IN, 'Check-in'),
        (PAYMENT, 'Payment'),
        (CHECK_OUT, 'Check-out'),
    )

    rental = models.ForeignKey(
        Rental,
        on_delete=models.PROTECT,   # что с этим делать?
        related_name='+',
    )

    type = models.IntegerField(choices=EVENT_CHOICES, default=0)

    def __str__(self):
        return 'id=%d type=%s' % (self.id, self.type)
