# Generated by Django 3.2.3 on 2021-05-29 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210529_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='setup',
            name='occupyTime',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
