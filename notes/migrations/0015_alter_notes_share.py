# Generated by Django 4.2.5 on 2023-12-06 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0014_notes_share'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='share',
            field=models.CharField(choices=[('False', 'Hayır'), ('True', 'Evet')], max_length=10),
        ),
    ]
