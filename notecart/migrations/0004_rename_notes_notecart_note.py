# Generated by Django 4.2.5 on 2023-11-23 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notecart', '0003_alter_notecart_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notecart',
            old_name='notes',
            new_name='note',
        ),
    ]
