# Generated by Django 2.2.1 on 2019-06-04 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subCityList', '0003_auto_20190603_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subcity',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
