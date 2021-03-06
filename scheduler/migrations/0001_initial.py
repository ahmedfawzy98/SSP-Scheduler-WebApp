# Generated by Django 2.2 on 2019-09-22 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('priority', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('term', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('creditHours', models.PositiveIntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('groupNum', models.PositiveIntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('type', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('PeriodType', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('type', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('ExPlace', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('PeriodType', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('type', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('PeriodType', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_day', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('time_from', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('time_to', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('ExDay', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('ExFrom', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('ExTo', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('lab', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Lab')),
                ('lecture', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Lecture')),
                ('tut', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Tutorial')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('priority', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('course', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Course')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='inst',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='scheduler.Instructor'),
        ),
    ]
