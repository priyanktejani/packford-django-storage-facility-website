# Generated by Django 4.0.1 on 2022-03-04 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('tax', models.FloatField()),
                ('order_total', models.FloatField()),
                ('monthly_charge', models.FloatField(blank=True, null=True)),
                ('schedule', models.CharField(blank=True, max_length=10, null=True)),
                ('schedule_duration', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=10)),
                ('is_ordered', models.BooleanField(default=False)),
                ('return_requested', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='clients.location')),
                ('company_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='clients.location')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('crate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.crate')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
