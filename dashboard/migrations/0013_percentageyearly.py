# Generated by Django 5.0.1 on 2024-01-24 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_percentagedata_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='PercentageYearly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('spr_per', models.FloatField()),
                ('gas_per', models.FloatField()),
                ('dist_per', models.FloatField()),
            ],
        ),
    ]