# Generated by Django 2.2 on 2021-06-08 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneaker_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
