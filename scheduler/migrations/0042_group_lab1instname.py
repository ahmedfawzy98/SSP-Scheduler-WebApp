# Generated by Django 2.2 on 2019-05-21 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0041_group_tut2periodtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='lab1InstName',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]
