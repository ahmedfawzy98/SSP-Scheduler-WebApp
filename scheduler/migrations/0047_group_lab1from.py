# Generated by Django 2.2 on 2019-05-21 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0046_group_lab1day'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='lab1From',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]