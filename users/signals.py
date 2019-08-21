from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Photographer

# pas oublier le apps.py
# il faut changer le settings
# 'users.apps.UsersConfig', sinon il ira pas chercher le signal
@receiver(post_save, sender=User) #post_save est le signal qu'on écoute
def create_photographer(sender, instance, created, **kwargs):
    if created:
        Photographer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_photographer(sender, instance, **kwargs):
    instance.photographer.save()


@receiver(post_delete, sender=Photographer)
def delete_image(sender, instance, **kwargs):
    if instance.image.name != "default.jpg":
        instance.image.delete(False)
