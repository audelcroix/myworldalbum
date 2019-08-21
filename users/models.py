from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
import os


def picture_rename(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    return f'profile_pics/profile_pic-{instance.user.username}{file_extension}'#.format(userid= instance.user.id, basename= basefilename, randomstring= randomstr, ext= file_extension)

class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(default='')
    image = models.ImageField(upload_to=picture_rename, default="default.jpg")


    def __str__(self):
        return f'{self.user.username} Photographer'

    def save(self, *args, **kwargs):
        value = self.user.username
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('photographer_home', args=[
            str(self.slug),
        ])
