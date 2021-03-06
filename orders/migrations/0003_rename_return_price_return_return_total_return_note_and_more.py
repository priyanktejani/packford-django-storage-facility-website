# Generated by Django 4.0.1 on 2022-03-05 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_return'),
    ]

    operations = [
        migrations.RenameField(
            model_name='return',
            old_name='return_price',
            new_name='return_total',
        ),
        migrations.AddField(
            model_name='return',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='return',
            name='pickup_date',
            field=models.DateField(default=None),
            preserve_default=False,
        ),
    ]
