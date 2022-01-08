# Generated by Django 3.1 on 2022-01-08 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storebot', '0030_auto_20211230_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordereditems',
            name='cart',
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='user_id',
            field=models.IntegerField(default=1, max_length=255, verbose_name='Client telegram Id si'),
            preserve_default=False,
        ),
    ]