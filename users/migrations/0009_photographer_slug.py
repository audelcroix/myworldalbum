# Generated by Django 2.2.1 on 2019-08-02 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190801_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographer',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
