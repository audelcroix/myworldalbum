# Generated by Django 2.2.1 on 2019-08-01 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190801_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photographer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]
