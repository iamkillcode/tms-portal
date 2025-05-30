# Generated by Django 5.1.4 on 2025-04-30 14:55

import django.db.models.deletion
from django.db import migrations, models


def create_initial_divisions(apps, schema_editor):
    Division = apps.get_model('tender_app', 'Division')
    divisions = [
        ('HR', 'HR Division'),
        ('ITMS', 'ITMS Division'),
        ('FIN', 'Finance Division'),
        ('CLSR', 'Centre for Laboratory Services and Research'),
        ('HPTD', 'Health Products and Technologies Division'),
        ('QMSD', 'Quality Assurance Division'), 
        ('CSD', 'Corporate Services Division'),
        ('FD', 'Food Division'),
    ]
    for code, name in divisions:
        Division.objects.create(code=code, name=name)


def reverse_divisions(apps, schema_editor):
    Division = apps.get_model('tender_app', 'Division')
    Division.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('tender_app', '0014_remove_isonumber_division_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(create_initial_divisions, reverse_divisions),
        migrations.AddField(
            model_name='isonumber',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tender_app.division'),
        ),
    ]
