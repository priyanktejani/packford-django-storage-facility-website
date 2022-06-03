# Generated by Django 4.0.1 on 2022-03-05 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_alter_crate_status_alter_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crate',
            name='status',
            field=models.CharField(choices=[('Shelf', 'Shelf'), ('Pick up room', 'Pick up room'), ('In transit', 'In transit'), ('Delivered', 'Delivered')], default='Shelf', max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('Shelf', 'Shelf'), ('Pick up room', 'Pick up room'), ('In transit', 'In transit'), ('Delivered', 'Delivered')], default='Shelf', max_length=30),
        ),
    ]
