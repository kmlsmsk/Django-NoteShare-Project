# Generated by Django 4.2.5 on 2023-12-21 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculumVitae', '0004_dynamicv_biolink'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicv',
            name='keywords',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]