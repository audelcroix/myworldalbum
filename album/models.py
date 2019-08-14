from django.db import models
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from users.models import Photographer
from PIL import Image


class Photo(models.Model):
    categories = [
        ("animal", "animal"),
        ("art", "art"),
        ("landscape", "landscape"),
        ("nature", "nature"),
        ("people", "people"),
        ("sky", "sky"),
    ]

    title = models.CharField(max_length=128, verbose_name='Title')
    description = models.TextField(max_length=6000, verbose_name='Description')
    category = models.CharField(max_length=16, choices=categories, default="art", verbose_name='Category')
    img = models.ImageField(upload_to='album/user_images')
    author = models.ForeignKey('users.Photographer', on_delete=models.CASCADE)

    slug = models.SlugField(default='', editable=False)

    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={"pk":self.pk})


class Comment(models.Model):
    content = models.TextField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey('users.Photographer', on_delete=models.CASCADE)
    article = models.ForeignKey('Photo', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content[:40]

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={"pk":self.pk})
    # def get_absolute_url(self):
    #     return reverse('homepage')
