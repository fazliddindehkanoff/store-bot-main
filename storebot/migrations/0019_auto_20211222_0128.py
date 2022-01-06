# Generated by Django 3.1 on 2021-12-22 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storebot', '0018_auto_20211222_0041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='buyAllItems',
        ),
        migrations.CreateModel(
            name='BuyAllItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=False, verbose_name='savatdagi barcha narsani sotib oladimi?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storebot.client')),
            ],
        ),
    ]