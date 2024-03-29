# Generated by Django 5.0.1 on 2024-01-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_builddrawheatmap'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryDiffHeatmap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('inventory_diff', models.FloatField()),
            ],
        ),
    ]
