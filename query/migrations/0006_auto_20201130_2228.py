# Generated by Django 3.1.3 on 2020-11-30 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0005_auto_20201130_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
