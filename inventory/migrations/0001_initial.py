# Generated by Django 4.0.1 on 2022-03-04 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Crate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crate_name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('delivery_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('storage_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('stock', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.company')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Warehouse name')),
                ('city', models.CharField(choices=[('London', 'New'), ('Sheffield', 'Accepted'), ('Liverpool', 'Completed'), ('Bristol', 'Sussex'), ('Hertfordshire', 'Hertfordshire'), ('Birmingham', 'Glasgow'), ('Wales', 'Wales'), ('Kent', 'Kent'), ('Leicester', 'Leicester'), ('Coventry', 'Coventry')], max_length=20)),
                ('crate_stock', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('delivery_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('storage_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('stock', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.company')),
                ('crate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.crate')),
            ],
        ),
        migrations.AddField(
            model_name='crate',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
    ]