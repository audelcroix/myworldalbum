# Generated by Django 2.2.1 on 2019-08-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='profile_pics', verbose_name='profile picture'),
        ),
    ]
