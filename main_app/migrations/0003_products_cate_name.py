# Generated by Django 3.0.4 on 2021-02-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210202_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='cate_name',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
    ]
