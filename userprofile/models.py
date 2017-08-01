from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from discount.models import Discount

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    phone = PhoneNumberField(blank=True)
    user_points = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    parent = models.OneToOneField(User, blank=True, null=True, related_name='childs')
    # user_num = models.CharField(max_length=50, blank=True, unique=True, default=str(uuid.uuid4()))

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     if not self.user_num:
    #         self.user_num = str(uuid.uuid4())
    #     super(models.Model, self).save(*args, **kwargs)

class PickUpRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    points = models.DecimalField(max_digits=8, decimal_places=2, null=True, default=0.00)
    requisites = models.CharField(max_length=256, default='')

    def __str__(self):
        return str(self.user.id)

    class Meta:
        verbose_name = 'PickUpRequest'
        verbose_name_plural = 'PickUpRequests'

def create_profile(sender, **kwargs):
    parent = kwargs['instance'].__dict__.get('parent')
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'], parent=parent)


post_save.connect(create_profile, sender=User)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


