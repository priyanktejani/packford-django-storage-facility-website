# Generated by Django 4.0.1 on 2022-03-05 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_remove_crate_warehouse_delete_warehouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='crate',
            name='status',
            field=models.CharField(choices=[('Shelf', 'shelf'), ('Pick-up room', 'pick-up room'), ('in transit', 'in transit'), ('delivered', 'delivered')], default='Shelf', max_length=30),
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('Shelf', 'shelf'), ('Pick-up room', 'pick-up room'), ('in transit', 'in transit'), ('delivered', 'delivered')], default='Shelf', max_length=30),
        ),
    ]
