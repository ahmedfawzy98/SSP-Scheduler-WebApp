# Generated by Django 2.2 on 2019-05-21 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0056_group_lab2to'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='lab2PeriodType',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]
