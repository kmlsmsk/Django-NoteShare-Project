# Generated by Django 4.2.5 on 2023-11-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_alter_notes_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='filePdf',
            field=models.FileField(default=24, upload_to='pdfs/'),
            preserve_default=False,
        ),
    ]
