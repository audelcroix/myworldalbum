# Generated by Django 2.2.1 on 2019-08-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190801_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
