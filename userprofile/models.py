from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from discount.models import Discount

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    user_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


