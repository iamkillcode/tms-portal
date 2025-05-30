# Generated by Django 5.1.4 on 2025-03-26 16:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tender_app', '0008_alter_tender_options_tender_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(max_length=255),
        ),
    ]
