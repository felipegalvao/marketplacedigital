from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='img/avatars')
    about = models.CharField(max_length=1000, blank=True)
    comission_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.10)
    activated = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expiration = models.DateTimeField(blank=True, null=True)
    payment_email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
