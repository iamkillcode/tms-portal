# Generated by Django 5.1.4 on 2025-05-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tender_app', '0017_vendor_tenderitem_frameworkagreement_vendorbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenderitem',
            name='appearance',
            field=models.CharField(blank=True, help_text='e.g., Colorless liquid', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='assay_percentage',
            field=models.CharField(blank=True, help_text='e.g., ≥99.8%', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='chemical_formula',
            field=models.CharField(blank=True, help_text='e.g., CH3COCH3', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='chemical_grade',
            field=models.CharField(blank=True, help_text='e.g., HPLC Grade, Analytical Reagent Grade', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='density',
            field=models.CharField(blank=True, help_text='e.g., 0.791 g/mL at 25°C', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='impurities',
            field=models.TextField(blank=True, help_text='List of impurity limits', null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='molar_mass',
            field=models.CharField(blank=True, help_text='e.g., 88.11 g/mol', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='package_size',
            field=models.CharField(blank=True, help_text='e.g., 2.5L, 500ml', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='physical_form',
            field=models.CharField(blank=True, help_text='e.g., Solvent, Powder, Crystal', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tenderitem',
            name='vapor_density',
            field=models.CharField(blank=True, help_text='e.g., 2 (vs air)', max_length=100, null=True),
        ),
    ]
