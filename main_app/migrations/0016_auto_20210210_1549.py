# Generated by Django 3.0.4 on 2021-02-10 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_auto_20210209_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='cust_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Customer'),
        ),
    ]
