# Generated by Django 4.2.5 on 2023-12-06 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0013_alter_notes_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='share',
            field=models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
