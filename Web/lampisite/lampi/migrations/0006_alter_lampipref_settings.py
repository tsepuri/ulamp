# Generated by Django 4.0.2 on 2022-04-28 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lampi', '0005_lampipref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lampipref',
            name='settings',
            field=models.CharField(default="{'color': {'h': 1, 's':1}, 'brightness': 1}", max_length=100),
        ),
    ]
