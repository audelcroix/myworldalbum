from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Photo


# pas oublier le apps.py
# il faut changer le settings
# 'users.apps.UsersConfig', sinon il ira pas chercher le signal

@receiver(post_delete, sender=Photo)
def photo_delete(sender, instance, **kwargs):
    instance.img.delete(False)
