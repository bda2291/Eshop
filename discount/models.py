from django.db import models
import uuid
from django.db.models.signals import post_save
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Discount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=50, blank=True, unique=True, default=str(uuid.uuid4()))
    valid_from = models.DateTimeField(default=datetime.now, blank=True)
    valid_to = models.DateTimeField(default=datetime.now()+timedelta(days=7), blank=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=10)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

def create_discount(sender, **kwargs):
    if kwargs['created']:
        user_discount = Discount.objects.create(user=kwargs['instance'])

post_save.connect(create_discount, sender=User)

User.discount = property(lambda u: Discount.objects.get_or_create(user=u)[0])

