# Generated by Django 5.1.4 on 2025-05-29 12:00
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('tender_app', '0021_userprofile_avatar_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenders', to='tender_app.vendor'),
        ),
    ]
