# Generated by Django 3.0.4 on 2021-02-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20210210_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='receipt_type',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
