# Generated by Django 5.0.1 on 2024-01-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('crude_stk', models.IntegerField()),
                ('crude_stk_spr', models.IntegerField()),
                ('gas_stk', models.IntegerField()),
                ('dist_stk', models.IntegerField()),
            ],
        ),
    ]
