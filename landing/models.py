from django.db import models

# Create your models here.
class Subscriber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'MySubsciber'
        verbose_name_plural = 'List of Subscribers'

    def __str__(self):
        try:
            return self.name
        except:
            return '{0!s}'.format(self.id)