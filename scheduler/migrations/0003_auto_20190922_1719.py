# Generated by Django 2.2 on 2019-09-22 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_auto_20190922_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='department',
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]