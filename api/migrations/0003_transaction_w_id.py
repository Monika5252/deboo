# Generated by Django 3.2.3 on 2021-06-23 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_userprofile_fcm_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='w_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_id', to='api.wallet'),
        ),
    ]