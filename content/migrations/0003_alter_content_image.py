# Generated by Django 4.2.5 on 2023-12-05 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_content_user_alter_content_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]