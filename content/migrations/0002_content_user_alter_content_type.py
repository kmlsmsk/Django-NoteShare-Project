# Generated by Django 4.2.5 on 2023-12-03 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('menu', 'menu'), ('haber', 'haber'), ('duyuru', 'duyuru'), ('etkinlik', 'etkinlik')], max_length=15),
        ),
    ]
