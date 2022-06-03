# Generated by Django 4.0.1 on 2022-03-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_crate_status_alter_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crate',
            name='status',
            field=models.CharField(choices=[('Shelf', 'Shelf'), ('Pick up room', 'Pick up room'), ('In transit', 'In transit'), ('Delivered', 'Delivered'), ('Return initiated', 'Return initiated')], default='Shelf', max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('Shelf', 'Shelf'), ('Pick up room', 'Pick up room'), ('In transit', 'In transit'), ('Delivered', 'Delivered'), ('Return initiated', 'Return initiated')], default='Shelf', max_length=30),
        ),
    ]
